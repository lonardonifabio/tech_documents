// Environment configuration for different deployment scenarios
export interface EnvironmentConfig {
  ollama: {
    baseUrl: string;
    defaultModel: string;
    maxRetries: number;
    retryDelay: number;
    maxTokens: number;
    temperature: number;
  };
  chat: {
    maxHistoryLength: number;
    suggestedQuestions: string[];
    welcomeMessage: string;
  };
  performance: {
    isGitHubPages: boolean;
    memoryLimit: string;
    responseTimeout: number;
  };
}

const getEnvironmentConfig = (): EnvironmentConfig => {
  // Detect if running on GitHub Pages or similar static hosting
  const isGitHubPages = 
    typeof window !== 'undefined' && 
    (window.location.hostname.includes('github.io') || 
     window.location.hostname.includes('githubpages.dev') ||
     window.location.hostname.includes('netlify.app') ||
     window.location.hostname.includes('vercel.app') ||
     window.location.hostname.includes('pages.dev') ||
     window.location.protocol === 'https:' && window.location.hostname !== 'localhost' ||
     process.env.GITHUB_PAGES === 'true');

  // Detect available memory (rough estimation)
  const getMemoryTier = (): 'low' | 'medium' | 'high' => {
    if (typeof navigator !== 'undefined' && 'deviceMemory' in navigator) {
      const deviceMemory = (navigator as any).deviceMemory;
      if (deviceMemory <= 4) return 'low';
      if (deviceMemory <= 8) return 'medium';
      return 'high';
    }
    // Default to medium for unknown environments
    return isGitHubPages ? 'low' : 'medium';
  };

  const memoryTier = getMemoryTier();

  // Model selection based on environment
  const getOptimalModel = (): string => {
    switch (memoryTier) {
      case 'low':
        return 'llama3.2:3b'; // Smallest, fastest
      case 'medium':
        return 'mistral:7b-instruct'; // Good balance
      case 'high':
        return 'llama3.1:8b'; // Best quality
      default:
        return 'mistral:7b-instruct';
    }
  };

  // Performance settings based on environment
  const getPerformanceSettings = () => {
    switch (memoryTier) {
      case 'low':
        return {
          maxTokens: 300,
          maxHistoryLength: 5,
          responseTimeout: 300000, // 300 seconds (5 minutes) for low memory environments
          retryDelay: 2000,
        };
      case 'medium':
        return {
          maxTokens: 500,
          maxHistoryLength: 10,
          responseTimeout: 300000, // 300 seconds (5 minutes) for medium memory
          retryDelay: 1500,
        };
      case 'high':
        return {
          maxTokens: 800,
          maxHistoryLength: 15,
          responseTimeout: 300000, // 300 seconds (5 minutes) for high memory
          retryDelay: 1000,
        };
      default:
        return {
          maxTokens: 500,
          maxHistoryLength: 10,
          responseTimeout: 300000, // Default 300 seconds (5 minutes)
          retryDelay: 1500,
        };
    }
  };

  const perfSettings = getPerformanceSettings();

  return {
    ollama: {
      baseUrl: process.env.OLLAMA_BASE_URL || 'http://localhost:11434',
      defaultModel: process.env.OLLAMA_DEFAULT_MODEL || getOptimalModel(),
      maxRetries: isGitHubPages ? 2 : 3,
      retryDelay: perfSettings.retryDelay,
      maxTokens: perfSettings.maxTokens,
      temperature: 0.7,
    },
    chat: {
      maxHistoryLength: perfSettings.maxHistoryLength,
      suggestedQuestions: [
        "What are the main topics covered in this document?",
        "Can you explain the key concepts mentioned?",
        "What is the main conclusion or takeaway?",
        "Who is the target audience for this document?",
        "Summarize the methodology described",
        "What are the practical applications mentioned?",
      ],
      welcomeMessage: "Hello! I'm here to help you understand and discuss this document. You can ask me questions about its content, key concepts, or request explanations of specific topics mentioned in the document.",
    },
    performance: {
      isGitHubSpaces: isGitHubPages,
      memoryLimit: memoryTier,
      responseTimeout: perfSettings.responseTimeout,
    },
  };
};

// Export singleton instance
export const environmentConfig = getEnvironmentConfig();

// Utility functions
export const isLowMemoryEnvironment = (): boolean => {
  return environmentConfig.performance.memoryLimit === 'low';
};

export const getRecommendedModels = (): string[] => {
  const { memoryLimit } = environmentConfig.performance;
  
  switch (memoryLimit) {
    case 'low':
      return ['llama3.2:3b', 'phi3:mini', 'mistral:7b-instruct'];
    case 'medium':
      return ['mistral:7b-instruct', 'llama3.2:3b', 'llama3.1:8b', 'codellama:7b'];
    case 'high':
      return ['llama3.1:8b', 'mistral:7b-instruct', 'codellama:7b', 'llama3.2:3b'];
    default:
      return ['mistral:7b-instruct', 'llama3.2:3b'];
  }
};

export const shouldShowPerformanceWarning = (): boolean => {
  return environmentConfig.performance.isGitHubSpaces || isLowMemoryEnvironment();
};

export const isGitHubPages = (): boolean => {
  return environmentConfig.performance.isGitHubSpaces;
};

// Debug information
export const getEnvironmentInfo = () => {
  return {
    isGitHubSpaces: environmentConfig.performance.isGitHubSpaces,
    memoryTier: environmentConfig.performance.memoryLimit,
    recommendedModel: environmentConfig.ollama.defaultModel,
    maxTokens: environmentConfig.ollama.maxTokens,
    maxHistory: environmentConfig.chat.maxHistoryLength,
    deviceMemory: typeof navigator !== 'undefined' && 'deviceMemory' in navigator 
      ? (navigator as any).deviceMemory 
      : 'unknown',
    userAgent: typeof navigator !== 'undefined' ? navigator.userAgent : 'unknown',
  };
};
