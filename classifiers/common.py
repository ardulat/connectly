TASK = """
    Rank query by intent.

    I would like to purchase a sofa => purchase_product

    What kind of toys for kids do you have? => ask_for_recommendation

    I would like to return a sofa => return_product

    Thank you so much => thank

"""

PRECLASSIFIER_MODEL_NAME = 'EthanChen0418/few-shot-model-five-classes'
POSTCLASSIFIER_MODEL_NAME = 'facebook/bart-large-mnli'
