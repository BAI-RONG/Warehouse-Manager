"""
LLM工具类 - 提供大模型调用和API接口
"""
import os
import asyncio
import aiohttp
from typing import List, Dict, Any, Optional, Union
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
import yaml
import json
from dataclasses import dataclass
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class LLMResponse:
    content: str
    usage: Dict[str, Any]
    model: str
    timestamp: str

class LLMTools:
    """大模型工具类"""
    
    def __init__(self, config_path: str = "/workspace/config/config.yaml"):
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
        
        self.llm_config = self.config['llm']
        self.llm = ChatOpenAI(
            model=self.llm_config['model'],
            temperature=self.llm_config['temperature'],
            max_tokens=self.llm_config['max_tokens'],
            api_key=self.llm_config.get('api_key', os.getenv('OPENAI_API_KEY'))
        )
    
    async def call_llm(self, 
                      prompt: str, 
                      system_prompt: str = "", 
                      temperature: Optional[float] = None) -> LLMResponse:
        """调用大模型"""
        try:
            messages = []
            if system_prompt:
                messages.append(SystemMessage(content=system_prompt))
            messages.append(HumanMessage(content=prompt))
            
            if temperature is not None:
                llm = ChatOpenAI(
                    model=self.llm_config['model'],
                    temperature=temperature,
                    max_tokens=self.llm_config['max_tokens'],
                    api_key=self.llm_config.get('api_key', os.getenv('OPENAI_API_KEY'))
                )
            else:
                llm = self.llm
            
            response = await llm.ainvoke(messages)
            
            return LLMResponse(
                content=response.content,
                usage=getattr(response, 'usage', {}),
                model=self.llm_config['model'],
                timestamp=str(asyncio.get_event_loop().time())
            )
        except Exception as e:
            logger.error(f"LLM调用失败: {e}")
            raise
    
    async def batch_call_llm(self, 
                            prompts: List[str], 
                            system_prompts: List[str] = None,
                            temperature: Optional[float] = None) -> List[LLMResponse]:
        """批量调用大模型"""
        if system_prompts is None:
            system_prompts = [""] * len(prompts)
        
        tasks = [
            self.call_llm(prompt, system_prompt, temperature)
            for prompt, system_prompt in zip(prompts, system_prompts)
        ]
        
        return await asyncio.gather(*tasks)
    
    def format_prompt(self, template: str, **kwargs) -> str:
        """格式化prompt模板"""
        try:
            prompt_template = PromptTemplate.from_template(template)
            return prompt_template.format(**kwargs)
        except Exception as e:
            logger.error(f"Prompt格式化失败: {e}")
            return template
    
    async def evaluate_response(self, 
                               response: str, 
                               criteria: Dict[str, str],
                               reference: str = "") -> Dict[str, float]:
        """评估响应质量"""
        evaluation_prompt = f"""
请根据以下标准评估这个响应的质量，给出0-1的分数：

响应内容：
{response}

参考标准：
{reference}

评估维度：
{json.dumps(criteria, ensure_ascii=False, indent=2)}

请以JSON格式返回评分结果，格式如下：
{{
    "dimension_name": score,
    "overall": average_score
}}
"""
        
        result = await self.call_llm(evaluation_prompt)
        try:
            scores = json.loads(result.content)
            return scores
        except:
            logger.warning("评估结果解析失败，返回默认分数")
            return {dim: 0.5 for dim in criteria.keys()}

class SearchTools:
    """联网搜索工具"""
    
    def __init__(self):
        self.session = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def search_web(self, query: str, num_results: int = 5) -> List[Dict[str, Any]]:
        """联网搜索"""
        # 这里可以集成真实的搜索API，如Google Search API、Bing Search API等
        # 暂时返回模拟结果
        return [
            {
                "title": f"搜索结果 {i+1}",
                "url": f"https://example.com/result_{i+1}",
                "snippet": f"关于'{query}'的相关信息 {i+1}",
                "relevance_score": 0.9 - i * 0.1
            }
            for i in range(num_results)
        ]
    
    async def get_context_from_search(self, query: str) -> str:
        """从搜索结果获取上下文"""
        results = await self.search_web(query)
        context = "\n".join([
            f"标题: {result['title']}\n内容: {result['snippet']}"
            for result in results[:3]
        ])
        return context

class DataProcessor:
    """数据处理工具"""
    
    @staticmethod
    def load_excel(file_path: str) -> Dict[str, Any]:
        """加载Excel文件"""
        import pandas as pd
        try:
            df = pd.read_excel(file_path)
            return {
                "data": df.to_dict('records'),
                "columns": df.columns.tolist(),
                "shape": df.shape
            }
        except Exception as e:
            logger.error(f"Excel文件加载失败: {e}")
            return {"data": [], "columns": [], "shape": (0, 0)}
    
    @staticmethod
    def save_jsonl(data: List[Dict[str, Any]], file_path: str):
        """保存为JSONL格式"""
        with open(file_path, 'w', encoding='utf-8') as f:
            for item in data:
                f.write(json.dumps(item, ensure_ascii=False) + '\n')
    
    @staticmethod
    def load_jsonl(file_path: str) -> List[Dict[str, Any]]:
        """加载JSONL文件"""
        data = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    data.append(json.loads(line.strip()))
        except Exception as e:
            logger.error(f"JSONL文件加载失败: {e}")
        return data