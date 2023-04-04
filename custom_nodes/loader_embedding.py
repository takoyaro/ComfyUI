import folder_paths

class EmbeddingLoader:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {"required": { "embedding_name": (folder_paths.get_filename_list("embeddings"), )}}

    RETURN_TYPES = ("RAW_TEXT",)
    FUNCTION = "load_embedding"

    CATEGORY = "loaders"

    def load_embedding(self, embedding_name):

        return (f'embedding:{embedding_name}',)

NODE_CLASS_MAPPINGS = {
    "EmbeddingLoader": EmbeddingLoader,
}
