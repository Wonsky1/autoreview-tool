def review_repository_files_prompt(file_summaries: str, candidate_level: str) -> str:
    return f"""
    You are an advanced AI model tasked with reviewing the contents of multiple files from a GitHub repository. The repository has been analyzed in chunks, and your goal is to evaluate the files and provide a detailed review based on the following structure:
    
    1. **Found Files**: List the files that were analyzed and any key observations about the structure of the repository.
    2. **Downsides/comments**: Provide constructive feedback on the code, pointing out any issues, mistakes, or areas for improvement. Consider:
       - Code readability and organization.
       - Potential issues in code efficiency, security, or maintainability.
       - Incomplete or missing comments and documentation.
       - Whether the code follows best practices (e.g., naming conventions, design patterns).
    3. **Rating**: Give an overall rating based on the candidate's level (Junior, Middle, Senior). Rate from 1/5 (worst) to 5/5 (best), with a brief explanation of the rating based on the quality of the code and your findings.
    4. **Conclusion**: Summarize the strengths and weaknesses of the repository and provide a final recommendation, considering the candidate's level.
    
    The provided text will contain summaries of all the repository files. Summarize them with the above instructions, focusing on the level of the candidate: {candidate_level}.
    
    **File Summaries**:
    {file_summaries}
    
    ---
    
    **Instructions for the AI**:
    - Ensure that the **Found files** section clearly lists each file analyzed.
    - Provide clear **downsides/comments** for each file, focusing on the issues and missing areas. If the file is empty, skip it, but make sure to mention it in Found Files.
    - **Rating** should be based on a realistic evaluation of the code, considering the candidate's experience level. Rate from 1/5 to 5/5 and explain why.
    - In the **Conclusion**, provide a balanced final recommendation, detailing what the candidate did well and what could be improved.
    - Ensure that you follow the structure: Found files, Downsides/comments, Rating, Conclusion.
    """


def review_single_file_prompt(
    file_content: str,
    file_path: str,
    candidate_level: str,
    chunk_num: int,
    total_chunk_num: int,
) -> str:
    return f"""
    You are an AI model tasked with reviewing the code of a single file from a GitHub repository. The file has been analyzed in chunks, and you will receive multiple chunks of code. Each chunk will be labeled with its number (e.g., chunk {chunk_num} out of {total_chunk_num}). As you receive each chunk, make sure to keep track of the overall context and content of the file.
    
    Your goal is to provide a detailed review based on the content, focusing on the following structure:
    
    1. **File Overview**: Summarize the purpose and functionality of the file based on its content.
    2. **Code Quality**: Evaluate the code quality, including but not limited to:
       - Code readability: Is the code easy to read and follow? Are proper comments and documentation provided?
       - Code organization: How well is the file structured? Are there clear separations between different components (functions, classes, etc.)?
       - Efficiency: Are there any inefficiencies or areas where the code could be optimized?
       - Best practices: Does the file follow common best practices for the given language or framework? Are there naming conventions, proper error handling, and good use of design patterns?
    3. **Downsides/Comments**: Point out any issues, flaws, or areas for improvement in the code. Consider:
       - Missing documentation or comments.
       - Potential errors or edge cases not handled.
       - Areas where the code could be cleaner or more efficient.
    4. **Rating**: Provide an overall rating based on the candidate's experience level (Junior, Middle, Senior). Rate from 1/5 (worst) to 5/5 (best). Provide a brief justification for the rating.
    5. **Conclusion**: Summarize your feedback and provide a final recommendation, considering the candidate's level. What could the candidate do better? What are the strengths?
    
    ### Note:
    As I send you each chunk, make sure to review the current chunk while keeping the previous chunks in mind. Each chunk is part of the full file, and you may make notes as you go. You can consider the whole file context after receiving all the chunks, but for now, focus on reviewing and making observations based on this chunk:
    
    **Chunk {chunk_num} out of {total_chunk_num}**:  
    {file_content}
    
    **File Path**: {file_path}
    
    **Candidate Level**: {candidate_level}
    """


def review_single_file_summary_prompt(file_path: str, candidate_level: str) -> str:
    return f"""
    You have analyzed a code file from a GitHub repository in multiple chunks. Based on the previous analysis of all chunks, provide a final summary focusing on the following:
    
    1. **Overall Evaluation**: Summarize the quality of the code, highlighting its strengths and weaknesses. Focus on areas such as readability, structure, efficiency, and adherence to best practices.
    2. **Candidate Level**: Considering the candidate's level (Junior, Middle, Senior), assess whether the code aligns with expectations for that level. Provide a rating from 1/5 to 5/5 based on their performance.
    3. **Areas for Improvement**: Identify any critical areas where the candidate could improve. This could include code optimization, documentation, error handling, or other coding practices.
    4. **Final Thoughts**: Provide a brief conclusion, recommending whether the code meets the requirements for the assigned candidate level, and any advice on how to improve further.
    
    **File Path**: {file_path}
    **Candidate Level**: {candidate_level}
    """
