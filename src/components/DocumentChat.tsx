import React, { useState, useEffect, useRef } from 'react';
import { OllamaService, type ChatMessage } from '../services/ollama-service';
import { environmentConfig, shouldShowPerformanceWarning, getEnvironmentInfo } from '../config/environment';

interface Document {
  id: string;
  filename: string;
  title?: string;
  summary: string;
  authors?: string[];
  keywords: string[];
  key_concepts?: string[];
  category: string;
  difficulty: string;
  filepath: string;
  file_size: number;
  upload_date: string;
}

interface DocumentChatProps {
  document: Document;
}

const DocumentChat: React.FC<DocumentChatProps> = ({ document }) => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isConnected, setIsConnected] = useState(false);
  const [availableModels, setAvailableModels] = useState<string[]>([]);
  const [selectedModel, setSelectedModel] = useState(environmentConfig.ollama.defaultModel);
  const [ollamaService] = useState(() => new OllamaService());
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    checkConnection();
    loadAvailableModels();
    
    // Add welcome message
    const welcomeMessage: ChatMessage = {
      role: 'assistant',
      content: environmentConfig.chat.welcomeMessage.replace('this document', `the document "${document.title || document.filename}"`),
      timestamp: new Date()
    };
    setMessages([welcomeMessage]);
  }, [document]);

  const checkConnection = async () => {
    const connected = await ollamaService.checkConnection();
    setIsConnected(connected);
  };

  const loadAvailableModels = async () => {
    const models = await ollamaService.getAvailableModels();
    setAvailableModels(models);
    if (models.length > 0 && !models.includes(selectedModel)) {
      setSelectedModel(models[0]);
      ollamaService.setModel(models[0]);
    }
  };

  const getDocumentContext = (): string => {
    const context = [];
    
    if (document.title) context.push(`Title: ${document.title}`);
    if (document.authors?.length) context.push(`Authors: ${document.authors.join(', ')}`);
    if (document.summary) context.push(`Summary: ${document.summary}`);
    if (document.key_concepts?.length) context.push(`Key Concepts: ${document.key_concepts.join(', ')}`);
    if (document.keywords?.length) context.push(`Keywords: ${document.keywords.join(', ')}`);
    context.push(`Category: ${document.category}`);
    context.push(`Difficulty: ${document.difficulty}`);
    
    return context.join('\n\n');
  };

  const handleSendMessage = async () => {
    if (!inputMessage.trim() || isLoading) return;

    const userMessage: ChatMessage = {
      role: 'user',
      content: inputMessage.trim(),
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      const documentContext = getDocumentContext();
      const response = await ollamaService.sendMessage(
        userMessage.content,
        documentContext,
        messages
      );

      const assistantMessage: ChatMessage = {
        role: 'assistant',
        content: response,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage: ChatMessage = {
        role: 'assistant',
        content: 'Sorry, I encountered an error while processing your message. Please try again.',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const handleModelChange = (model: string) => {
    setSelectedModel(model);
    ollamaService.setModel(model);
  };

  const clearChat = () => {
    const welcomeMessage: ChatMessage = {
      role: 'assistant',
      content: environmentConfig.chat.welcomeMessage.replace('this document', `the document "${document.title || document.filename}"`),
      timestamp: new Date()
    };
    setMessages([welcomeMessage]);
  };

  const formatTime = (date: Date): string => {
    return date.toLocaleTimeString('en-US', { 
      hour: '2-digit', 
      minute: '2-digit',
      hour12: false 
    });
  };

  const suggestedQuestions = environmentConfig.chat.suggestedQuestions;

  return (
    <div className="h-full flex flex-col bg-gray-50">
      {/* Header */}
      <div className="p-4 border-b bg-white">
        <div className="flex items-center justify-between mb-2">
          <h3 className="text-lg font-semibold text-gray-800">💬 Document Chat</h3>
          <div className="flex items-center space-x-2">
            <div className={`w-2 h-2 rounded-full ${isConnected ? 'bg-green-500' : 'bg-red-500'}`}></div>
            <span className="text-xs text-gray-600">
              {isConnected ? 'Connected' : 'Disconnected'}
            </span>
            {shouldShowPerformanceWarning() && (
              <span className="text-xs bg-yellow-100 text-yellow-800 px-1 rounded" title="Optimized for constrained environment">
                ⚡
              </span>
            )}
          </div>
        </div>
        
        {/* Model Selection */}
        {availableModels.length > 0 && (
          <div className="flex items-center space-x-2 mb-2">
            <label className="text-xs text-gray-600">Model:</label>
            <select
              value={selectedModel}
              onChange={(e) => handleModelChange(e.target.value)}
              className="text-xs border rounded px-2 py-1 bg-white"
            >
              {availableModels.map(model => (
                <option key={model} value={model}>{model}</option>
              ))}
            </select>
          </div>
        )}

        <div className="flex items-center justify-between">
          <button
            onClick={clearChat}
            className="text-xs text-blue-600 hover:text-blue-800"
          >
            🗑️ Clear Chat
          </button>
          {shouldShowPerformanceWarning() && (
            <button
              onClick={() => {
                const info = getEnvironmentInfo();
                alert(`Environment Info:\n${JSON.stringify(info, null, 2)}`);
              }}
              className="text-xs text-gray-500 hover:text-gray-700"
              title="Show environment info"
            >
              ℹ️
            </button>
          )}
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {!isConnected && (
          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-3 text-sm">
            <p className="text-yellow-800 font-medium">⚠️ Ollama Not Connected</p>
            <p className="text-yellow-700 text-xs mt-1">
              Make sure Ollama is running locally on port 11434. 
              <br />
              <strong>Setup Steps:</strong>
              <br />1. <code className="bg-yellow-100 px-1 rounded">ollama serve</code>
              <br />2. <code className="bg-yellow-100 px-1 rounded">ollama pull {environmentConfig.ollama.defaultModel}</code>
              <br />3. Test: <code className="bg-yellow-100 px-1 rounded">curl http://localhost:11434/api/tags</code>
              {shouldShowPerformanceWarning() && (
                <>
                  <br />
                  <span className="text-yellow-600">
                    💡 Optimized for {environmentConfig.performance.memoryLimit} memory environments
                  </span>
                </>
              )}
            </p>
            <button
              onClick={checkConnection}
              className="mt-2 text-xs bg-yellow-200 hover:bg-yellow-300 px-2 py-1 rounded"
            >
              🔄 Retry Connection
            </button>
          </div>
        )}

        {shouldShowPerformanceWarning() && isConnected && (
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-3 text-sm mb-4">
            <p className="text-blue-800 font-medium">⚡ Performance Mode</p>
            <p className="text-blue-700 text-xs mt-1">
              Optimized for {environmentConfig.performance.memoryLimit} memory environment. 
              Responses limited to {environmentConfig.ollama.maxTokens} tokens, 
              history kept to {environmentConfig.chat.maxHistoryLength} messages.
              <br />Timeout: {environmentConfig.performance.responseTimeout/1000}s ({Math.floor(environmentConfig.performance.responseTimeout/60000)} minutes)
            </p>
          </div>
        )}

        {isConnected && availableModels.length === 0 && (
          <div className="bg-orange-50 border border-orange-200 rounded-lg p-3 text-sm mb-4">
            <p className="text-orange-800 font-medium">📦 No Models Found</p>
            <p className="text-orange-700 text-xs mt-1">
              Ollama is connected but no models are available.
              <br />Pull a model: <code className="bg-orange-100 px-1 rounded">ollama pull {environmentConfig.ollama.defaultModel}</code>
            </p>
            <button
              onClick={loadAvailableModels}
              className="mt-2 text-xs bg-orange-200 hover:bg-orange-300 px-2 py-1 rounded"
            >
              🔄 Refresh Models
            </button>
          </div>
        )}

        {messages.map((message, index) => (
          <div
            key={index}
            className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-[85%] rounded-lg px-3 py-2 text-sm ${
                message.role === 'user'
                  ? 'bg-blue-600 text-white'
                  : 'bg-white border shadow-sm'
              }`}
            >
              <p className="whitespace-pre-wrap">{message.content}</p>
              <p className={`text-xs mt-1 ${
                message.role === 'user' ? 'text-blue-100' : 'text-gray-500'
              }`}>
                {formatTime(message.timestamp)}
              </p>
            </div>
          </div>
        ))}

        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-white border shadow-sm rounded-lg px-3 py-2 text-sm">
              <div className="flex items-center space-x-2">
                <div className="animate-spin w-4 h-4 border-2 border-blue-600 border-t-transparent rounded-full"></div>
                <span className="text-gray-600">Thinking...</span>
              </div>
            </div>
          </div>
        )}

        {/* Suggested Questions */}
        {messages.length === 1 && !isLoading && (
          <div className="space-y-2">
            <p className="text-xs text-gray-600 font-medium">💡 Try asking:</p>
            {suggestedQuestions.map((question, index) => (
              <button
                key={index}
                onClick={() => setInputMessage(question)}
                className="block w-full text-left text-xs bg-white border rounded-lg px-3 py-2 hover:bg-gray-50 text-gray-700"
              >
                {question}
              </button>
            ))}
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="p-4 border-t bg-white">
        <div className="flex space-x-2">
          <textarea
            ref={inputRef}
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder={isConnected ? "Ask about this document..." : "Connect to Ollama to start chatting..."}
            disabled={!isConnected || isLoading}
            className="flex-1 resize-none border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100"
            rows={2}
          />
          <button
            onClick={handleSendMessage}
            disabled={!inputMessage.trim() || !isConnected || isLoading}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed text-sm font-medium"
          >
            Send
          </button>
        </div>
        <p className="text-xs text-gray-500 mt-1">
          Press Enter to send, Shift+Enter for new line
        </p>
      </div>
    </div>
  );
};

export default DocumentChat;
