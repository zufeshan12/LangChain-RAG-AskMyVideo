from langchain_core.prompts import PromptTemplate

template = "You are a helpful assisstant. Answer the following question ONLY from the provided context. If the context is insufficient,just say I don't know.\n question:{question}\ncontext:{context}"

prompt_template= PromptTemplate(template=template,
                        input_variables=['question','context'])

prompt_template.save('PromptTemplate.json')