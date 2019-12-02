def result_to_dict(results):
    dict_list = []

    for row in results:
        result_dict = dict(row)
        dict_list.append(result_dict)
     
    return dict_list
