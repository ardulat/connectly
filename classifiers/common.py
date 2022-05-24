TASK = """
Rank query by intent.

I would like to purchase a sofa => purchase_product

I would like to purchase a sofa, thanks => purchase_product

I would like to buy a recommended item => purchase_product

Can I buy a recommended sofa? Thanks in advance => purchase_product

What kind of toys for kids do you have? => ask_for_recommendation

Can you recommend me a sofa? Thanks in advance => ask_for_recommendation

I would like to return a sofa => return_product

Can I return a book? Thanks a lot => return_product

Thank you so much => thank

Thanks a lot! => thank

"""

PRECLASSIFIER_MODEL_NAME = 'EthanChen0418/few-shot-model-five-classes'
POSTCLASSIFIER_MODEL_NAME = 'facebook/bart-large-mnli'
