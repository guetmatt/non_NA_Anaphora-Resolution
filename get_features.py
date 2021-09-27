"""
MATTHIAS GUETEBIER
Matr.-Nr.: 108016243375

Modul mit Funktionen zur Feature-Extraktion fuer den Klassifizierer.
"""






### WENN ante_index == 1 UND anaph_index == 2 ###
### --> IST DIE DISTANZ ZWISCHEN TOKEN / SAETZEN DANN = 0 ODER = 1 ????


def get_tok_dist_training(coref_dict):
    """
    Menge an Token zwischen Antezedens und Anapher aus Trainingsdaten extrahieren.

    :param coref_dict: Dict

    :return: tok_dist: Integer
    """


    for doc in coref_dict:
        for dd_ent in coref_dict[doc]:

            # HIER EVTL FUER ANTE DOCH DEN ANFANGSINDEX NEHMEN UND NICHT DEN ENDINDEX
            # SONST KOMMT BEI EINGEBETTETEN ANAPHs EINE NEGATIVE DISTANZ RAUS
            ante_index = coref_dict[doc][dd_ent]["elements"][0][0][1]
            anaph_index = coref_dict[doc][dd_ent]["elements"][-1][0][0]

            coref_dict[doc][dd_ent]["tok_dist"] = anaph_index - ante_index

    return coref_dict




def get_sent_dist_training(coref_dict):
    """
    Menge an Saetzen zwischen Antezedens und Anapher aus Trainingsdaten extrahiern.
    
    :param coref_dict: 
    :return: 
    """

    for doc in coref_dict:
        for dd_ent in coref_dict[doc]:

            ante_index = coref_dict[doc][dd_ent]["elements"][0][1]
            anaph_index = coref_dict[doc][dd_ent]["elements"][-1][1]

            coref_dict[doc][dd_ent]["sent_dist"] = anaph_index - ante_index

    return coref_dict



# def get_form_anaph_training(coref_dict):
#     """
#     Linguistische Form des anaphorischen Ausdrucks aus Trainingsdaten extrahieren.
#
#     :param coref_dict:
#     :return:
#     """
#
#     for doc in coref_dict


