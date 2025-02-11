const axios = require('axios');
const cheerio = require('cheerio');

class WebTool {
  constructor() {
    this.client = axios.create({
      headers: {
        'User-Agent': 'Mozilla/5.0 (compatible; AnalyticsBot/1.0)',
        'Accept': 'text/html,application/json,application/xhtml+xml'
      },
      timeout: 30000
    });
  }

  async makeRequest(url, {
    method = 'GET',
    params = null,
    data = null,
    headers = null,
    timeout = null
  } = {}) {
    try {
      const response = await this.client.request({
        method: method.toUpperCase(),
        url,
        params,
        data,
        headers: { ...this.client.defaults.headers, ...headers },
        timeout: timeout || this.client.defaults.timeout
      });

      return {
        success: true,
        status: response.status,
        data: response.data,
        headers: response.headers,
        metadata: {
          url: response.config.url,
          method: response.config.method,
          timestamp: new Date().toISOString()
        }
      };
    } catch (error) {
      return {
        success: false,
        error: error.message,
        metadata: {
          url,
          method,
          timestamp: new Date().toISOString()
        }
      };
    }
  }

  async scrapeWebpage(url, { selectors = null, extractLinks = false } = {}) {
    try {
      const response = await this.makeRequest(url);
      if (!response.success) {
        throw new Error(response.error);
      }

      const $ = cheerio.load(response.data);
      const result = {
        title: $('title').text(),
        content: {}
      };

      if (selectors) {
        selectors.forEach(selector => {
          result.content[selector] = $(selector).text();
        });
      } else {
        result.content.text = $('body').text();
      }

      if (extractLinks) {
        result.links = [];
        $('a').each((_, element) => {
          const href = $(element).attr('href');
          if (href) {
            result.links.push({
              text: $(element).text(),
              url: href
            });
          }
        });
      }

      return {
        success: true,
        data: result,
        metadata: {
          url,
          timestamp: new Date().toISOString()
        }
      };
    } catch (error) {
      return {
        success: false,
        error: error.message,
        metadata: {
          url,
          timestamp: new Date().toISOString()
        }
      };
    }
  }

  async monitorEndpoint(url, { interval = 60, maxAttempts = 5 } = {}) {
    const results = [];
    let attempts = 0;

    while (attempts < maxAttempts) {
      const result = await this.makeRequest(url);
      results.push({
        timestamp: new Date().toISOString(),
        success: result.success,
        status: result.status,
        responseTime: result.metadata?.responseTime
      });

      attempts++;
      if (attempts < maxAttempts) {
        await new Promise(resolve => setTimeout(resolve, interval * 1000));
      }
    }

    return {
      url,
      monitoring_period: {
        start: results[0].timestamp,
        end: results[results.length - 1].timestamp
      },
      results
    };
  }
}

module.exports = WebTool;