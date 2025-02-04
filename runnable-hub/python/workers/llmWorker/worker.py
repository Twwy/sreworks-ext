import json
from re import L
from runnable import RunnableWorker, RunnableContext, RunnableStatus, RunnableOutputLoads
from .request.llmRequest import LlmRequest
from .response.llmResponse import LlmResponse, LlmMessage, LlmUsage
import aiohttp

class Worker(RunnableWorker):

    runnableCode = "LLM_WORKER"
    Request = LlmRequest
    Response = LlmResponse

    def __init__(self):
        pass

    async def onNext(self, context: RunnableContext[LlmRequest, LlmResponse]) -> RunnableContext:
        headers = {
            "Authorization": f"Bearer {context.request.secretKey}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": context.request.model,
            "messages":[{
                "role": "system",
                "content": context.request.systemPrompt
            }]
        }
        for message in context.request.history:
            payload["messages"].append({
                "role": message.role,
                "content": message.content
            })
        payload["messages"].append({
            "role": "user",
            "content": context.request.userPrompt
        })

        async with aiohttp.ClientSession() as session:
            async with session.post(context.request.endpoint, 
                                    headers=headers, json=payload) as response:
                result = await response.json()
                message = LlmMessage(
                    role=result["choices"][0]["message"]["role"],
                    content=result["choices"][0]["message"]["content"]
                )
                sendMessage = LlmMessage(
                    role="user",
                    content=context.request.userPrompt,
                )
                usage = LlmUsage(
                    promptTokens=result["usage"]["prompt_tokens"],
                    completionTokens=result["usage"]["completion_tokens"],
                    totalTokens=result["usage"]["total_tokens"]
                )
                context.response = LlmResponse(
                    message=message,
                    usage=usage,
                    sendMessage=sendMessage,
                )
                context.status = RunnableStatus.SUCCESS
                return context


  



