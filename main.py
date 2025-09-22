"""
模块名：服务主模块-main.py
模块说明：
- 服务主模块
"""
from langchain_core.runnables import RunnableBranch, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from config import Config


def get_qa_history_chain():
    llm = ChatOpenAI(
        api_key=Config["llm_api_key"],
        base_url=Config["api_base_url"],
        model_name=Config["default_model"],
        temperature=Config["default_temperature"]
    )
    condense_question_system_template = (
        "请根据聊天记录总结用户最近的问题，"
        "如果没有多余的聊天记录则返回用户的问题。"
    )
    condense_question_prompt = ChatPromptTemplate([
        ("system", condense_question_system_template),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
    ])

    history_branch = RunnableBranch(
        # 分支 1: 若聊天记录中没有 chat_history 则直接使用用户问题
        (lambda x: not x.get("chat_history", False), (lambda x: x["input"]),),
        # 分支 2 : 若聊天记录中有 chat_history 则先让 llm 根据聊天记录完善问题
        condense_question_prompt | llm | StrOutputParser(),
    )

    system_prompt = (
        "你是一个问答任务的助手。 "
        "请使用检索到的上下文片段回答这个问题。 "
        "如果你不知道答案就说不知道。 "
        "请使用简洁的话语回答用户。"
        "\n\n"
        "{context}"
    )
    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("placeholder", "{chat_history}"),
            ("human", "{input}"),
        ]
    )

    qa_chain = (qa_prompt | llm | StrOutputParser())

    qa_history_chain = RunnablePassthrough.assign(
        context=(lambda x: x) | history_branch  # 将查询结果存为 content
    ).assign(answer=qa_chain)  # 将最终结果存为 answer

    return qa_history_chain


def gen_response(chain, input, chat_history):
    response = chain.invoke({
        "input": input,
        "chat_history": chat_history
    })
    return response['answer']
    # for res in response:
    #     if "answer" in res.keys():
    #         yield res["answer"]


def main():
    messages = []
    while (prompt := input()) != 'END':
        print(messages)
        messages.append(("human:", prompt))

        answer = gen_response(
            chain=get_qa_history_chain(),
            input=prompt,
            chat_history=messages
        )

        messages.append(("ai", answer))
        print(answer)


if __name__ == "__main__":
    main()
