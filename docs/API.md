# H-XZ-V2 API Documentation

## Pentest Scanner API

### PentestScanner Class

```python
from scripts.pentest import PentestScanner

scanner = PentestScanner(target="192.168.1.1", output_file="results.json")
results = scanner.run_scan()
```

#### Methods

**`scan_ports()`**
- Scans for open ports on the target
- Returns: List of open ports with service information
- Uses nmap or fallback socket scanning

**`check_ssl_tls()`**
- Checks SSL/TLS configuration
- Returns: List of SSL/TLS vulnerabilities

**`check_common_vulnerabilities()`**
- Checks for common misconfigurations
- Returns: List of detected vulnerabilities

**`run_scan()`**
- Executes full pentest scan
- Returns: Complete results dictionary

**`save_results()`**
- Saves results to JSON file

## AI Analysis API

### GeminiAnalyzer Class

```python
from scripts.ai_analyzer import GeminiAnalyzer

analyzer = GeminiAnalyzer(api_key="your_api_key")
analysis = analyzer.analyze_vulnerability(vulnerability_dict)
```

#### Methods

**`analyze_vulnerability(vulnerability: Dict) -> Dict`**
- Analyzes a single vulnerability using Google Gemini
- Parameters:
  - `vulnerability`: Dictionary with vulnerability details
- Returns: Analyzed vulnerability with AI recommendations

**`analyze_results(results: Dict) -> Dict`**
- Analyzes all vulnerabilities in results
- Parameters:
  - `results`: Complete pentest results dictionary
- Returns: Analysis with risk score and recommendations

### GroqAnalyzer Class

```python
from scripts.ai_analyzer import GroqAnalyzer

analyzer = GroqAnalyzer(api_key="your_api_key")
analysis = analyzer.analyze_vulnerability(vulnerability_dict)
```

#### Methods

Same as GeminiAnalyzer but uses Groq API instead.

## Results Format

### JSON Output Structure

```json
{
  "timestamp": "2024-06-20T15:30:00",
  "target": "192.168.1.1",
  "open_ports": [
    {
      "port": 22,
      "protocol": "tcp",
      "service": "ssh",
      "state": "open"
    }
  ],
  "vulnerabilities": [
    {
      "type": "exposed_database",
      "port": 3306,
      "severity": "critical",
      "description": "MySQL database exposed on port 3306",
      "ai_analysis": {
        "risk_explanation": "...",
        "attack_vectors": ["..."],
        "remediation": ["..."]
      }
    }
  ],
  "summary": {
    "total_open_ports": 5,
    "total_vulnerabilities": 3,
    "critical": 1,
    "high": 1,
    "medium": 1
  }
}
```

## Environment Variables

```bash
# For Gemini API
export GEMINI_API_KEY="your_gemini_api_key"

# For Groq API
export GROQ_API_KEY="your_groq_api_key"
```

## Examples

### Basic Scan

```bash
python scripts/pentest.py --target 192.168.1.1 --output results.json
```

### Scan with AI Analysis

```bash
python scripts/pentest.py --target 192.168.1.1 --output results.json --ai-analysis
```

### Programmatic Usage

```python
from scripts.pentest import PentestScanner
from scripts.ai_analyzer import GeminiAnalyzer
import json

# Run scan
scanner = PentestScanner(target="192.168.1.1")
results = scanner.run_scan()

# Analyze with AI
analyzer = GeminiAnalyzer()
analysis = analyzer.analyze_results(results)

# Save combined results
results["ai_analysis"] = analysis
with open("full_results.json", "w") as f:
    json.dump(results, f, indent=2)
```

## Error Handling

### Missing API Keys

```python
try:
    analyzer = GeminiAnalyzer()
except ValueError as e:
    print(f"Error: {e}")
    # Fallback to basic analysis
```

### Network Errors

The scanner includes fallback mechanisms:
- If nmap is unavailable, uses socket scanning
- If AI API fails, provides fallback analysis

## Rate Limiting

- Gemini API: Check Google's documentation for rate limits
- Groq API: Check Groq's documentation for rate limits

## Security Considerations

1. **API Keys**: Never commit API keys to version control
2. **Target Authorization**: Only scan targets you own or have permission to test
3. **Data Privacy**: Results may contain sensitive information
4. **Compliance**: Follow responsible disclosure practices

## Support

For issues or questions, open an issue on GitHub: https://github.com/OffModzKkkkj/H-XZ-V2/issues
