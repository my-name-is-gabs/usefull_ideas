'''
The concept is that before inserting the data in filter_constraint function they must be cleaned up. Meaning they need to be converted before passing it to the dynamic filtering function.

The bt system has multiple models that is needed to be used for filtering. The challenge is how to unify them
Take note, you cannot combine in a single query builder a db column from a different Model.

remember this reference for ideal filter destructure
conditions = [User.age > 18, User.name == "Alice"]
query = session.query(User).filter(*conditions)


'''

class Model1:
    @staticmethod
    def samp():
        print("hello")
        
class Model2:
    @staticmethod
    def samp():
        print("test")
        
recipe_1 = {
    "Model1": {
        "model": Model1,
        "fields": [
            "dateFrom",
            "vvip"
        ],
    },
    "Model2": {
        "model": Model2,
        "fields": [
            "bt_status"
        ],
       
    }
}

recipe_2 = {
    "dateFrom": {
        "type": "comparison",
        "field": "date_from",
        "operator": "greater_than",
        "value": None
    },
    "vvip": {
        "type": "comparison",
        "field": "vvip",
        "operator": "equals",
        "value": None
    },
    "bt_status": {
        "type": "IN",
        "field": "bt_status",
        "value": None
    }
}


def query_builder(comparison_json, model):
    print("================================")
    return f"the model {model}, the comparison {comparison_json}"
    
# def json_combiner_and_builder(type_, comparisons):
#     combinator_json = {
#         "comparison": {
#             "type": "AND",
#             "comparisons": comparisons
#         }
#     }

def filter_constraint(models, **kwargs):
    obj_data = kwargs
        
    the_models = models
    
    for model in models:
        for value in recipe_1[model]["fields"]:
            recipe_2[value]["value"] = obj_data[value]

    # print("the recipe modefied", recipe_2)
    
    multiple_query = []
    
    for model_name in models:
        for field_name in recipe_1[model_name]["fields"]:
            multiple_query.append(
                query_builder(comparison_json=recipe_2[field_name], model=model_name)
            )
                
    
    print("Apply this combine filter by destructuring it for example .join().filter(*multiple_query) ", *multiple_query)
    
filter_constraint(models=["Model1", "Model2"], dateFrom='2025-01-01', vvip=1, bt_status="Planning")




