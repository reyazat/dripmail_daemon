#!/usr/bin/python

class DripAction:
    main = 0
    resend = 1
    fallowup = 2
    extra = 3
    
class NextDrip(object):
    def __init__(self):
        None
        
    #def decide(self,elapsed_days,drip_action,numvisit,numclick,subscribe):
    def decide(self,list_of_dic_depend_emails):        
        main = [element for element in list_of_dic_depend_emails if element['iddripaction'] == DripAction.main ]
        resend = [element for element in list_of_dic_depend_emails if element['iddripaction'] == DripAction.resend]
        fallowup = [element for element in list_of_dic_depend_emails if element['iddripaction'] == DripAction.fallowup]
        extra = [element for element in list_of_dic_depend_emails if element['iddripaction'] == DripAction.extra]

        email = {}
        if main != [] and main[0]['checked'] == 0:  email = main[0]
        if resend != [] and  resend[0]['checked'] == 0: email = resend[0]
        if fallowup != [] and  fallowup[0]['checked'] == 0: email = fallowup[0]
        if extra != [] and extra[0]['checked'] == 0: email = extra[0]
        print email
        # In every situation, if user subscribes, we'll send thank you 
        if email['subscribe'] == True: return 'T'
        
        week_no = 1
        if email['elapsed_days'] > 21:  week_no = 4
        if email['elapsed_days'] > 14:  week_no = 3
        if email['elapsed_days'] > 7:  week_no = 2

        # if 4 weeks passed and user clicks or visits no other action will be done
        if week_no == 4:
            if email['numclick']  > 0: return 'end'
            if email['numvisit']  > 0: return 'end'
            else: return 'end'                    

        if week_no == 1:
            if email['numclick']  > 0: 
                if extra is None: return 'E'
                else: return 'end' 
            if email['numvisit']  > 0: return 'F'
            else: return 'R'    
        if week_no == 2:
            if email['numclick']  > 0: return 'E'
            if email['numvisit']  > 0: 
                if email['drip_action']  == 'extra': return 'E'
                if email['drip_action'] == 'fallowup': return 'F'
                if email['drip_action'] == 'resend': return 'F'
                if email['drip_action'] == 'main': return 'F'
            else: 
                if email['drip_action'] == 'extra': return 'E'
                if email['drip_action'] == 'fallowup': return 'F'
                if email['drip_action'] == 'resend': return 'R'
                if email['drip_action'] == 'main': return 'R'
        if week_no == 3:
            if email['numclick']  > 0: return 'E'
            if email['numvisit']  > 0: return 'E'
            if email['numvisit']  == 0: 
                if email['drip_action'] == 'fallowup': return 'E'
                else: return 'end'
