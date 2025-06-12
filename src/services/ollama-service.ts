import { environmentConfig } from '../config/environment';

interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

interface OllamaResponse {
  model: string;
  created_at: string;
  message: {
    role: string;
    content: string;
  };
  done: boolean;
}

class OllamaService {
  private baseUrl: string;
  private model: string;
  private maxRetries: number;
  private retryDelay: number;
  private maxTokens: number;
  private temperature: number;
  private responseTimeout: number;

  constructor(
    baseUrl: string = environmentConfig.ollama.baseUrl, 
    model: string = environmentConfig.ollama.defaultModel
  ) {
    this.baseUrl = baseUrl;
    this.model = model;
    this.maxRetries = environmentConfig.ollama.maxRetries;
    this.retryDelay = environmentConfig.ollama.retryDelay;
    this.maxTokens = environmentConfig.ollama.maxTokens;
    this.temperature = environmentConfig.ollama.temperature;
    this.responseTimeout = environmentConfig.performance.responseTimeout;
  }

  async checkConnection(): Promise<boolean> {
    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 5000); // 5 second timeout

      const response = await fetch(`${this.baseUrl}/api/tags`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
        signal: controller.signal,
      });

      clearTimeout(timeoutId);
      return response.ok;
    } catch (error) {
      console.warn('Ollama connection failed:', error);
      return false;
    }
  }

  async sendMessage(
    message: string, 
    documentContext: string = '',
    conversationHistory: ChatMessage[] = []
  ): Promise<string> {
    console.log('🤖 Sending message to Ollama:', { message, model: this.model, baseUrl: this.baseUrl });
    
    const systemPrompt = documentContext 
      ? `You are an AI assistant helping users understand and discuss a document. Here is the document context:

DOCUMENT CONTEXT:
${documentContext}

Please answer questions about this document and help users understand its content. Be concise but informative. If asked about something not in the document, politely indicate that and offer to help with what is available in the document.`
      : 'You are a helpful AI assistant. Please provide concise and accurate responses.';

    // Limit conversation history based on environment
    const historyLimit = environmentConfig.chat.maxHistoryLength;
    const messages = [
      { role: 'system', content: systemPrompt },
      ...conversationHistory.slice(-historyLimit).map(msg => ({
        role: msg.role,
        content: msg.content
      })),
      { role: 'user', content: message }
    ];

    // Use a more generous timeout - AI responses can take time
    const requestTimeout = Math.max(30000, this.responseTimeout); // At least 30 seconds
    
    for (let attempt = 0; attempt < this.maxRetries; attempt++) {
      try {
        console.log(`🔄 Attempt ${attempt + 1}/${this.maxRetries}`);
        
        const controller = new AbortController();
        const timeoutId = setTimeout(() => {
          console.log('⏰ Request timeout after', requestTimeout, 'ms');
          controller.abort();
        }, requestTimeout);

        // Simplified request body - some Ollama versions are picky about options
        const requestBody = {
          model: this.model,
          messages: messages,
          stream: false,
          options: {
            temperature: this.temperature,
            num_predict: this.maxTokens,
          }
        };

        console.log('📤 Request body:', JSON.stringify(requestBody, null, 2));

        const response = await fetch(`${this.baseUrl}/api/chat`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          signal: controller.signal,
          body: JSON.stringify(requestBody),
        });

        clearTimeout(timeoutId);

        console.log('📥 Response status:', response.status, response.statusText);

        if (!response.ok) {
          const errorText = await response.text();
          console.error('❌ Response error:', errorText);
          throw new Error(`HTTP error! status: ${response.status}, body: ${errorText}`);
        }

        const data: OllamaResponse = await response.json();
        console.log('✅ Response received:', data);
        
        if (!data.message || !data.message.content) {
          throw new Error('Invalid response format from Ollama');
        }
        
        return data.message.content;

      } catch (error) {
        console.error(`❌ Attempt ${attempt + 1} failed:`, error);
        
        if (attempt === this.maxRetries - 1) {
          if (error instanceof Error && error.name === 'AbortError') {
            return `Response timeout after ${requestTimeout/1000} seconds. The AI model might be loading or the question is too complex. Try:\n\n1. Asking a simpler question\n2. Waiting for the model to fully load\n3. Checking if Ollama is running: "ollama list"`;
          }
          if (error instanceof Error && error.message.includes('HTTP error')) {
            return `Connection error: ${error.message}\n\nPlease check:\n1. Ollama is running: "ollama serve"\n2. Model is available: "ollama list"\n3. Try pulling the model: "ollama pull ${this.model}"`;
          }
          return `Sorry, I'm having trouble connecting to the AI service. Error: ${error instanceof Error ? error.message : 'Unknown error'}\n\nPlease check if Ollama is running locally.`;
        }
        
        // Exponential backoff with jitter
        const delay = this.retryDelay * Math.pow(2, attempt) + Math.random() * 1000;
        console.log(`⏳ Waiting ${delay}ms before retry...`);
        await new Promise(resolve => setTimeout(resolve, delay));
      }
    }

    return 'Unable to get response from AI service after multiple attempts.';
  }

  async getAvailableModels(): Promise<string[]> {
    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 5000);

      const response = await fetch(`${this.baseUrl}/api/tags`, {
        signal: controller.signal,
      });
      
      clearTimeout(timeoutId);
      
      if (!response.ok) return [];
      
      const data = await response.json();
      const availableModels = data.models?.map((model: any) => model.name) || [];
      
      // Return models sorted by recommendation for current environment
      const recommended = environmentConfig.performance.memoryLimit === 'low' 
        ? ['llama3.2:3b', 'phi3:mini', 'mistral:7b-instruct']
        : ['mistral:7b-instruct', 'llama3.2:3b', 'llama3.1:8b', 'codellama:7b'];
      
      // Sort available models by recommendation order
      return availableModels.sort((a: string, b: string) => {
        const aIndex = recommended.findIndex(model => a.includes(model.split(':')[0]));
        const bIndex = recommended.findIndex(model => b.includes(model.split(':')[0]));
        
        if (aIndex === -1 && bIndex === -1) return 0;
        if (aIndex === -1) return 1;
        if (bIndex === -1) return -1;
        return aIndex - bIndex;
      });
    } catch (error) {
      console.error('Failed to get available models:', error);
      return [];
    }
  }

  setModel(model: string): void {
    this.model = model;
  }

  getModel(): string {
    return this.model;
  }
}

export { OllamaService, type ChatMessage };
