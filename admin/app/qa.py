import os
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

class ICHGuidelineQA:
    def __init__(self, persist_directory="/vectorstore/ich_db"):
        """
        ICHガイドラインのQ&Aシステムを初期化
        
        Args:
            persist_directory (str): ベクトルストアのディレクトリパス
        """
        if not os.path.exists(persist_directory):
            raise ValueError(f"Vector store directory not found: {persist_directory}")
            
        self.embeddings = HuggingFaceEmbeddings(
            model_name="intfloat/multilingual-e5-large",
            model_kwargs={'device': 'cpu'}
        )
        
        # ベクトルストアの読み込み
        try:
            self.vectorstore = Chroma(
                persist_directory=persist_directory,
                embedding_function=self.embeddings
            )
        except Exception as e:
            raise RuntimeError(f"Failed to load vector store: {str(e)}")

        # ChatGPTの初期化
        self.llm = ChatOpenAI(
            temperature=0,
            model_name="gpt-4o-mini-2024-07-18"
        )

        # プロンプトテンプレートの設定
        self.template = """あなたは医薬品規制のエキスパートです。
ICHガイドラインの内容に基づいて、質問に対して正確かつ専門的に回答してください。

参照コンテキスト:
{context}

質問: {question}

回答の際の注意点:
- ICHガイドラインの内容に基づいて回答してください
- ガイドラインの該当部分があれば、それを明示的に参照してください
- 推測が必要な場合は、その旨を明記してください
- 専門用語には必要に応じて簡潔な説明を加えてください

回答:"""

        self.prompt = ChatPromptTemplate.from_template(self.template)

        # Retrieverの設定
        self.retriever = self.vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={
                "k": 3
            }
        )

        # RAGチェーンの構築
        self.rag_chain = (
            {"context": self.retriever, "question": RunnablePassthrough()}
            | self.prompt
            | self.llm
            | StrOutputParser()
        )

    def answer_question(self, question: str) -> str:
        """
        質問に対する回答を生成
        
        Args:
            question (str): ユーザーからの質問
            
        Returns:
            str: 生成された回答
            
        Raises:
            Exception: RAG処理中にエラーが発生した場合
        """
        try:
            return self.rag_chain.invoke(question)
        except Exception as e:
            raise Exception(f"Failed to generate answer: {str(e)}")

    def get_relevant_sources(self, question: str) -> list:
        """
        関連する参照元を取得
        
        Args:
            question (str): ユーザーからの質問
            
        Returns:
            list: 関連する参照元のリスト
            
        Raises:
            Exception: 検索中にエラーが発生した場合
        """
        try:
            docs = self.vectorstore.similarity_search(
                question, 
                k=3)
            sources = []
            used_chunks = set()
            
            for doc in docs:
                if not hasattr(doc, 'metadata'):
                    continue
                    
                chunk_preview = doc.page_content[:500].replace('\n', ' ').strip()
                
                if chunk_preview not in used_chunks:
                    used_chunks.add(chunk_preview)
                    
                    source = {
                        'title': doc.metadata.get('title', 'タイトル不明'),
                        'code': doc.metadata.get('code', 'コード不明'),
                        'category': doc.metadata.get('category', 'カテゴリ不明'),
                        'source_file': doc.metadata.get('source_file'),
                        'preview': chunk_preview
                    }
                    sources.append(source)
            
            return sources
            
        except Exception as e:
            raise Exception(f"Failed to retrieve relevant sources: {str(e)}")