import asyncio 
from core.graph_engine import WorkFlowEngine
from logger import logger


async def split_text(state):
    """
    Docstring for split_text

    This function is used to split the given text whenever we encounter a "Fullstop (.)"
    :param state: State is a dictonary that is used to carry the name of the state associated with a node as key and the result of the node as value in the dictonary.
    """
    logger.info("Running Tool : Splitting(Text into chuncks)")
    text = state.get("input_text","")
    chunks = [s.strip() for s in text.split(".") if s]
    state["Splitted Text"] = chunks
    return state

async def summarize_chunks(state):
    """
    Docstring for summarize_chunks
    This function is used to summarize each chunk of the data that was splitted in previous phase.
    
    :param state: State is a dictonary that is used to carry the name of the state associated with a node as key and the result of the node as value in the dictonary.

    """
    logger.info("Running Tool: Summarizing Chunks")
    chunks = state.get("Splitted Text")
    summaries = []

    # Just taking top 4 words of each chuck to show that how summarizing will work
    # Here we can used LLM's or Transformers(Encoder-Decoder) to generate the summries.
    for chunk in chunks:
        words = chunk.split()
        short = " ".join(words[:3])
        summaries.append(short)

    state["summaries"] = summaries
    return state

async def merge_summaries(state):
    """
    Docstring for merge_summaries

    This function is used to merge summaries of all the chunks that are created in splitting node.
    
    :param state: State is a dictonary that is used to carry the name of the state associated with a node as key and the result of the node as value in the dictonary.
    """
    logger.info("Running Tool : Merging Summaries")
    merged_summary = " ".join(state["summaries"])
    state["current_summary"] = merged_summary
    state["current_length"] = len(merged_summary)
    return state


async def refine_summary(state):
    """
    Docstring for refine_summary

    This function is used to refine the summary to a certain limit 
    limit : any value less than text size, default 50 character 
    
    :param state: State is a dictonary that is used to carry the name of the state associated with a node as key and the result of the node as value in the dictonary.
    """
    text = state["current_summary"]
    current_len = len(text)
    limit = state.get("length_limit",50)

    logger.info(f"Running Tool: Refining the Summary. Length {current_len}, Target: {limit}")

    if current_len > limit:
        cut_point = int(current_len*0.9)
        state["current_summary"] = text[:cut_point]

    state["current_length"] = len(state["current_summary"])
    return state


def length_check(state):
    """
    Docstring for length_check

    This function is the condition function for the node refin_summary. It loops over till the lenght of the summary is under limit provided.
    
    :param state: State is a dictonary that is used to carry the name of the state associated with a node as key and the result of the node as value in the dictonary.
    """
    length = state["current_length"]
    limit = state.get("length_limit",50)

    if length > limit:
        logger.info("Text too long.Looping Back to Refine.")
        return "refine"
    else:
        logger.info("Length is in the range.")


def create_summary_agent():
    """
    Docstring for create_summary_agent

    This is function that creates a summary agent that have process 
    1.input_text
    2.split_text in chunks.
    3.summarize each chunk and store the result.
    4.merge the summary of each chunk.
    5.refine summary in the limit of the character
    """
    app = WorkFlowEngine()


    # Adding the nodes 
    app.add_node("split", split_text)
    app.add_node("summarize",summarize_chunks)
    app.add_node("merge",merge_summaries)
    app.add_node("refine",refine_summary)

    # Adding Edges
    app.add_edge("split","summarize")
    app.add_edge("summarize","merge")
    app.add_edge("merge","refine")

    # Adding a condition of Length of the summary
    app.add_condition("refine",length_check)

    return app


summary_bot = create_summary_agent()