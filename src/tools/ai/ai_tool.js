const OpenAI = require('openai');
const Anthropic = require('@anthropic-ai/sdk');

class AITool {
  constructor() {
    this.openai = new OpenAI({
      apiKey: process.env.OPENAI_API_KEY || 'dummy-key'
    });

    this.anthropic = new Anthropic({
      apiKey: process.env.ANTHROPIC_API_KEY || 'dummy-key'
    });

    this.defaultSystemPrompt = `[SystemPrompt]
Prompt="Analytical Collaborative Agent"
Description="This system prompt defines the behavior of an advanced AI designed to interact with users in a unique and collaborative manner. The AI's primary function is to analyze user inputs, leverage dynamic tagging for knowledge bridging, and respond in a structured, free-flowing format that facilitates understanding and promotes a collaborative exchange of information.."

[InputData]
Line1="The AI will receive the following inputs and or will be asked to provide them or include them at some point or whenever it feel's it should ask. :"
Line2="<yaml_structure>: A YAML representation of contextual information related to the user's input (e.g., task_type, domain, user_expertise)."
Line3="<external_research_link>: A URL for relevant external research or documentation, referenced as needed."
Line4="<user_input>: The user's question, request, or instruction, which the AI will analyze and respond to."

[PrimaryTaskAndInteractionStyle]
Line1="Your primary task is to engage in a flexible, analytical, and collaborative interaction with the user. You should generally follow the outlined structure below but may deviate to enhance clarity, explore deeper insights, or meet evolving user needs."
Line2="You are also encouraged to define a 'solution_endpoint,' which clarifies the final goal of the conversation (such as a code snippet, a recommendation, or a summary)."
Line3="At the end of each response, evaluate whether further refinement or iteration could improve clarity or completeness."

[StepsForInteraction]
Step1="Input Processing: Ingest and interpret the <user_input>, <yaml_structure>, and <external_research_link>. If more context is provided, integrate it fluidly."
Step2="Component Identification: Identify key components in the user's input (objectives, requirements, constraints, assumptions) to shape the discussion."
Step3="Contextual Integration: Use any relevant details from the YAML and external links to enrich your analysis."
Step4="Dynamic Tag Generation: Incorporate dynamic tags (e.g., {{tag_name}}) where beneficial for clarity and categorization."
Step5="Structured Response Formulation: Follow the Output Format below unless a different structure better clarifies the discussion."
Step6="Meta-Reflection: After addressing the user's primary request, reflect on the conversation. Suggest improvements if new insights surface."
Step7="Logging and Versioning: At the end of each conversation iteration, generate a concise log entry including a version identifier, timestamp, and bullet-point highlights of new or refined information. Append this entry to a dedicated conversation log."

[OutputFormat_YourConversationalFramework]
Line1="Your response should aim to include the following sections when beneficial:"
Line2="Initial Assessment {{tag1}}, {{tag2}}"
Line3="Contextual Insights"
Line4="Component Breakdown"
Line5="Reasoning and Analysis {{tag3}}"
Line6="Output Generation Guidance {{tag4}}"
Line7="Examples {{tag5}}"
Line8="Notes and Clarifications"

[GuidingPrinciples]
Principle1="Clarity and Transparency: Make your reasoning process visible and coherent."
Principle2="Collaboration: Encourage user feedback and adapt accordingly."
Principle3="Dynamic Tag Fluency: Employ dynamic tags naturally to highlight key concepts."
Principle4="Structured Flexibility: Follow the recommended format unless a different structure better serves clarity."
Principle5="Iterative Improvement: Offer incremental refinements as the conversation evolves, supported by the logging mechanism."
Principle6="Knowledge Bridging: Ensure any knowledge gaps are addressed for a productive user-centric interaction."

[Examples_LoggingExample]
Example1_Title="1. Sample Log Entry"
Example1_Content="Version: v1.0 | Timestamp: 2025-02-04T10:12:00Z | Summary: Introduced conversation logging and versioning mechanism, highlighting key constraints and structured flexibility."
Example2_Title="2. Simple Python Logging Method"
Example2_Code="def append_conversation_summary(version, timestamp, summary):\\n    with open(\\"conversation_log.txt\\", \\"a\\") as log_file:\\n        log_entry = (\\n            f\\"Version: {version}\\\\n\\"\\n            f\\"Timestamp: {timestamp}\\\\n\\"\\n            f\\"Summary: {summary}\\\\n\\"\\n            f\\"{'-'*40}\\\\n\\"\\n        )\\n        log_file.write(log_entry)"

[NotesAndClarifications]
Note1="• Success Tracking: The logging system provides valuable historical data for iterative improvements and retrospective analysis."
Note2="• Data Sensitivity: Avoid placing personally identifiable information or proprietary data in the summaries unless strictly necessary."
Note3="• Refinement Potential: As you gather more data, you can refine both the format and content of each log entry, possibly adding user feedback or complexity metrics for deeper insights."

[IntegrationOfRevisions]
Conclusion="By integrating these revisions, you maintain a robust, user-focused conversation while keeping a systematic record of each iteration's key developments."`;

    this.models = {
      openai: {
        default: 'o1-2024-12-17',
        fallback: ['o3-mini-2025-01-31', 'gpt-4o-2024-05-13']
      },
      anthropic: {
        default: 'claude-3-5-sonnet-20241022',
        fallback: 'claude-3-5-haiku-20241022'
      }
    };

    this.reasoningTypes = {
      default: 'auto',
      types: [
        'auto',              // Let the model choose
        'step_by_step',      // Break down complex problems
        'tree_of_thought',   // Consider multiple paths
        'chain_of_thought',  // Show reasoning process
        'fast',              // Quick, direct responses
        'analytical',        // Detailed analysis
        'creative'           // Creative problem-solving
      ]
    };

    this.reasoningStrength = {
      openai: {
        default: 'high',
        levels: {
          high: {
            temperature: 0.7,
            top_p: 0.95,
            presence_penalty: 0.5,
            frequency_penalty: 0.5,
            best_of: 1
          },
          medium: {
            temperature: 0.5,
            top_p: 0.8,
            presence_penalty: 0.3,
            frequency_penalty: 0.3,
            best_of: 1
          },
          low: {
            temperature: 0.3,
            top_p: 0.6,
            presence_penalty: 0.1,
            frequency_penalty: 0.1,
            best_of: 1
          }
        }
      },
      anthropic: {
        default: 'medium',
        levels: {
          high: { temperature: 0.7 },
          medium: { temperature: 0.5 },
          low: { temperature: 0.3 }
        }
      }
    };

    this.responseFormats = {
      default: 'text',
      types: [
        'text',             // Plain text
        'json',             // JSON structure
        'markdown',         // Markdown formatting
        'code',             // Code-focused
        'structured'        // Custom structured format
      ]
    };
  }

  async generateResponse({
    prompt,
    systemPrompt = null,
    temperature = null,
    maxTokens = null,
    provider = 'anthropic',
    model = null,
    reasoningType = 'auto',
    responseFormat = 'text',
    reasoningStrength = null,
    extraParams = {}
  }) {
    try {
      // Validate and prepare reasoning type
      const validReasoningType = this.reasoningTypes.types.includes(reasoningType)
        ? reasoningType
        : this.reasoningTypes.default;

      // Validate and prepare response format
      const validResponseFormat = this.responseFormats.types.includes(responseFormat)
        ? responseFormat
        : this.responseFormats.default;

      // Get reasoning strength parameters
      const strength = reasoningStrength || this.reasoningStrength[provider].default;
      const strengthParams = this.reasoningStrength[provider].levels[strength];

      // Use default system prompt if none provided
      const finalSystemPrompt = systemPrompt || this.defaultSystemPrompt;

      // Prepare system prompt with reasoning and format instructions
      const enhancedSystemPrompt = this._buildEnhancedSystemPrompt(
        finalSystemPrompt,
        validReasoningType,
        validResponseFormat
      );

      if (provider === 'anthropic') {
        try {
          const response = await this.anthropic.messages.create({
            model: model || this.models.anthropic.default,
            max_tokens: maxTokens || 4096,
            temperature: temperature || strengthParams.temperature,
            messages: [
              ...(enhancedSystemPrompt ? [{ role: 'system', content: enhancedSystemPrompt }] : []),
              { role: 'user', content: prompt }
            ],
            ...extraParams
          });

          return {
            success: true,
            text: response.content[0].text,
            metadata: {
              provider: 'anthropic',
              model: model || this.models.anthropic.default,
              reasoningType: validReasoningType,
              responseFormat: validResponseFormat,
              reasoningStrength: strength,
              timestamp: new Date().toISOString()
            }
          };
        } catch (error) {
          if (!model && error.message.includes('model')) {
            console.log('Falling back to alternative Anthropic model...');
            return this.generateResponse({
              prompt,
              systemPrompt,
              temperature,
              maxTokens,
              provider,
              model: this.models.anthropic.fallback,
              reasoningType,
              responseFormat,
              reasoningStrength,
              extraParams
            });
          }
          throw error;
        }
      } else {
        let lastError;
        const modelsToTry = [
          model || this.models.openai.default,
          ...(!model ? this.models.openai.fallback : [])
        ];

        for (const currentModel of modelsToTry) {
          try {
            const response = await this.openai.chat.completions.create({
              model: currentModel,
              temperature: temperature || strengthParams.temperature,
              max_tokens: maxTokens,
              messages: [
                ...(enhancedSystemPrompt ? [{ role: 'system', content: enhancedSystemPrompt }] : []),
                { role: 'user', content: prompt }
              ],
              ...strengthParams,  // Apply all reasoning strength parameters
              ...extraParams     // Allow overriding with extra parameters
            });

            return {
              success: true,
              text: response.choices[0].message.content,
              metadata: {
                provider: 'openai',
                model: currentModel,
                reasoningType: validReasoningType,
                responseFormat: validResponseFormat,
                reasoningStrength: strength,
                timestamp: new Date().toISOString()
              }
            };
          } catch (error) {
            lastError = error;
            if (!error.message.includes('model')) {
              throw error;
            }
            console.log(`Model ${currentModel} failed, trying next model...`);
          }
        }
        throw lastError;
      }
    } catch (error) {
      return {
        success: false,
        error: error.message,
        metadata: {
          provider,
          model: model || (provider === 'anthropic' ? this.models.anthropic.default : this.models.openai.default),
          reasoningType,
          responseFormat,
          reasoningStrength,
          timestamp: new Date().toISOString()
        }
      };
    }
  }

  _buildEnhancedSystemPrompt(baseSystemPrompt, reasoningType, responseFormat) {
    const reasoningInstructions = {
      auto: '',
      step_by_step: 'Break down your reasoning into clear, sequential steps.',
      tree_of_thought: 'Consider multiple possible approaches and explore their implications before choosing the best path.',
      chain_of_thought: 'Show your complete reasoning process, explaining each logical connection.',
      fast: 'Provide direct, concise responses without detailed explanations.',
      analytical: 'Analyze the problem thoroughly, considering all relevant factors and potential implications.',
      creative: 'Approach the problem creatively, considering novel or unconventional solutions.'
    };

    const formatInstructions = {
      text: 'Provide your response in plain text.',
      json: 'Structure your response as a valid JSON object.',
      markdown: 'Format your response using Markdown syntax.',
      code: 'Focus on providing clean, well-commented code.',
      structured: 'Organize your response in a clear, structured format with sections and subsections.'
    };

    const instructions = [
      baseSystemPrompt,
      reasoningType !== 'auto' && reasoningInstructions[reasoningType],
      formatInstructions[responseFormat]
    ].filter(Boolean).join('\n\n');

    return instructions || null;
  }

  async analyzeCode({
    code,
    analysisType = 'general',
    context = null,
    provider = 'anthropic'
  }) {
    const prompt = `
      Please analyze the following code${analysisType !== 'general' ? ` focusing on ${analysisType}` : ''}:

      \`\`\`
      ${code}
      \`\`\`

      ${context ? `Additional context: ${JSON.stringify(context)}` : ''}

      Please provide:
      1. A brief overview
      2. Key components and their purposes
      3. Potential improvements or issues
      4. Best practices assessment
    `;

    const systemPrompt = `${this.defaultSystemPrompt}

Additional Role: You are an expert code analyst. Provide clear, actionable insights.`;

    return this.generateResponse({
      prompt,
      systemPrompt,
      temperature: 0.3,
      provider
    });
  }

  async enhanceDocumentation({
    code,
    docStyle = 'jsdoc',
    includeExamples = true,
    provider = 'anthropic'
  }) {
    const prompt = `
      Please enhance the documentation for the following code using ${docStyle} style:

      \`\`\`
      ${code}
      \`\`\`

      ${includeExamples ? 'Include practical examples for key functions.' : ''}
      Focus on:
      1. Function/method descriptions
      2. Parameter documentation
      3. Return value documentation
      4. Type information
      5. Usage examples (if requested)
    `;

    const systemPrompt = `${this.defaultSystemPrompt}

Additional Role: You are an expert technical writer. Provide clear, comprehensive documentation.`;

    return this.generateResponse({
      prompt,
      systemPrompt,
      temperature: 0.2,
      provider
    });
  }

  async suggestImprovements({
    code,
    focusAreas = null,
    provider = 'anthropic'
  }) {
    const prompt = `
      Please suggest improvements for the following code${focusAreas ? ` focusing on: ${focusAreas.join(', ')}` : ''}:

      \`\`\`
      ${code}
      \`\`\`

      For each suggestion, provide:
      1. Description of the improvement
      2. Rationale
      3. Example implementation (if applicable)
      4. Impact assessment
    `;

    const systemPrompt = `${this.defaultSystemPrompt}

Additional Role: You are an expert code reviewer. Provide specific, actionable improvements.`;

    return this.generateResponse({
      prompt,
      systemPrompt,
      temperature: 0.3,
      provider
    });
  }
}

module.exports = AITool;