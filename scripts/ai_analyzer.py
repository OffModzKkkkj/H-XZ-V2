#!/usr/bin/env python3
"""
H-XZ-V2: AI-Powered Vulnerability Analysis
Integrates Google Gemini and Groq for intelligent vulnerability analysis
"""

import json
import os
from typing import Dict, List, Optional
from abc import ABC, abstractmethod

class AIAnalyzer(ABC):
    """Base class for AI analyzers"""
    
    @abstractmethod
    def analyze_vulnerability(self, vulnerability: Dict) -> Dict:
        """Analyze a single vulnerability"""
        pass
    
    def analyze_results(self, results: Dict) -> Dict:
        """Analyze all vulnerabilities in results"""
        analysis = {
            "vulnerabilities_analyzed": [],
            "recommendations": [],
            "risk_score": 0
        }
        
        for vuln in results.get("vulnerabilities", []):
            analyzed = self.analyze_vulnerability(vuln)
            analysis["vulnerabilities_analyzed"].append(analyzed)
        
        # Calculate overall risk score
        severity_scores = {
            "critical": 10,
            "high": 7,
            "medium": 4,
            "low": 1
        }
        
        total_score = sum(
            severity_scores.get(v.get("severity", "low"), 1)
            for v in results.get("vulnerabilities", [])
        )
        
        analysis["risk_score"] = min(100, total_score)
        
        return analysis


class GeminiAnalyzer(AIAnalyzer):
    """Google Gemini-based vulnerability analyzer"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment")
        
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-pro')
        except ImportError:
            print("[!] google-generativeai not installed. Install with: pip install google-generativeai")
            self.model = None
    
    def analyze_vulnerability(self, vulnerability: Dict) -> Dict:
        """Analyze vulnerability using Gemini"""
        if not self.model:
            return self._fallback_analysis(vulnerability)
        
        prompt = f"""
        Analyze this security vulnerability and provide:
        1. A brief explanation of the risk
        2. Potential attack vectors
        3. Remediation steps
        
        Vulnerability:
        Type: {vulnerability.get('type', 'unknown')}
        Severity: {vulnerability.get('severity', 'unknown')}
        Description: {vulnerability.get('description', 'N/A')}
        Port: {vulnerability.get('port', 'N/A')}
        
        Provide a JSON response with keys: "risk_explanation", "attack_vectors", "remediation"
        """
        
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text
            
            # Try to parse JSON from response
            try:
                analysis = json.loads(response_text)
            except:
                analysis = {
                    "risk_explanation": response_text,
                    "attack_vectors": [],
                    "remediation": []
                }
            
            return {
                **vulnerability,
                "ai_analysis": analysis
            }
        except Exception as e:
            print(f"[!] Gemini analysis failed: {e}")
            return self._fallback_analysis(vulnerability)
    
    def _fallback_analysis(self, vulnerability: Dict) -> Dict:
        """Fallback analysis when Gemini is unavailable"""
        return {
            **vulnerability,
            "ai_analysis": {
                "risk_explanation": "AI analysis unavailable",
                "attack_vectors": [],
                "remediation": ["Enable API key and try again"]
            }
        }


class GroqAnalyzer(AIAnalyzer):
    """Groq-based vulnerability analyzer"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in environment")
        
        try:
            from groq import Groq
            self.client = Groq(api_key=self.api_key)
        except ImportError:
            print("[!] groq not installed. Install with: pip install groq")
            self.client = None
    
    def analyze_vulnerability(self, vulnerability: Dict) -> Dict:
        """Analyze vulnerability using Groq"""
        if not self.client:
            return self._fallback_analysis(vulnerability)
        
        prompt = f"""
        Analyze this security vulnerability and provide:
        1. A brief explanation of the risk
        2. Potential attack vectors
        3. Remediation steps
        
        Vulnerability:
        Type: {vulnerability.get('type', 'unknown')}
        Severity: {vulnerability.get('severity', 'unknown')}
        Description: {vulnerability.get('description', 'N/A')}
        Port: {vulnerability.get('port', 'N/A')}
        
        Provide a JSON response with keys: "risk_explanation", "attack_vectors", "remediation"
        """
        
        try:
            message = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model="mixtral-8x7b-32768",
                temperature=0.7,
                max_tokens=1024
            )
            
            response_text = message.choices[0].message.content
            
            # Try to parse JSON from response
            try:
                analysis = json.loads(response_text)
            except:
                analysis = {
                    "risk_explanation": response_text,
                    "attack_vectors": [],
                    "remediation": []
                }
            
            return {
                **vulnerability,
                "ai_analysis": analysis
            }
        except Exception as e:
            print(f"[!] Groq analysis failed: {e}")
            return self._fallback_analysis(vulnerability)
    
    def _fallback_analysis(self, vulnerability: Dict) -> Dict:
        """Fallback analysis when Groq is unavailable"""
        return {
            **vulnerability,
            "ai_analysis": {
                "risk_explanation": "AI analysis unavailable",
                "attack_vectors": [],
                "remediation": ["Enable API key and try again"]
            }
        }


def analyze_results(results: Dict, ai_provider: str = "gemini") -> Dict:
    """Analyze pentest results using specified AI provider"""
    
    if ai_provider.lower() == "gemini":
        analyzer = GeminiAnalyzer()
    elif ai_provider.lower() == "groq":
        analyzer = GroqAnalyzer()
    else:
        raise ValueError(f"Unknown AI provider: {ai_provider}")
    
    return analyzer.analyze_results(results)


if __name__ == "__main__":
    # Example usage
    sample_vulnerability = {
        "type": "exposed_database",
        "port": 3306,
        "severity": "critical",
        "description": "MySQL database exposed on port 3306"
    }
    
    try:
        analyzer = GeminiAnalyzer()
        analysis = analyzer.analyze_vulnerability(sample_vulnerability)
        print(json.dumps(analysis, indent=2))
    except ValueError as e:
        print(f"Error: {e}")
