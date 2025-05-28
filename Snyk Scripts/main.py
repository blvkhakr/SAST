import pr_check_script , snyk_api

opt_list = ['0', '1', '2', '3']
bu_dict = {'Ancestry': 'business_unit_1', 'Ancestry-Sox':'business_unit_2', 'Ancestry-PCI':'business_unit_3', 'Ancestry-DNA':'business_unit_3', 'Ancestry-PetDNA':'business_unit_3', 'Ancestry-Genomics':'business_unit_3' } # ADD BU OPTIONS HERE
rp_list = ['m', 'M', 'd', 'D', 'exit']
ans_list = ['Yes', 'No']

try:
    user_input = input("Welcome to the Snyk API Script.\n What is this related to? Admin Work [ 1 ], PR Checks [ 2 ], GitHub [ 3 ], exit [0]:" )
    while user_input != '0':
        if user_input not in opt_list:
            user_input = input("That's not an option. Your options are Admin Work [ 1 ], PR Checks [ 2 ], GitHub [ 3 ], exit [0]: ")

        #
        # USER CHECK MAKE SURE DEAD USERS DONT EXIST
        # MAKE SURE 
        elif user_input == '1':
           rp_answer = input(f"What do you want to check? Dead Users [1], [2]")
           user_input = input("Want to do something else? Admin Work [1], PR Checks [2], GitHub [3], exit [0]:  ")
            

        elif user_input == "2":
            rp_answer = input("Which Do You Need To Do: Kill PR Check ['K'], Check Logs ['C'], or Quit ['Q']: ")

            if rp_answer.upper() == 'Q':
                print("Exiting PR Checks....")
                user_input = input("What is this related to? Admin Work [ 1 ], PR Checks [ 2 ], GitHub [ 3 ], exit [0]: ")
        
            elif rp_answer.upper() == 'K':
                orgs = snyk_api.get_Snyk_orgs()
                options = ','.joins(orgs)
                print(options)
                target_org = input(f"Which Org is this for?, {options}")
                bu = bu_dict.values
                print(bu)
                
               # unit = input("Which Org is this for? ['Ancestry, Ancestry-Sox, Ancestry-PCI, Ancestry-DNA, Ancestry-PetDNA, Ancestry-Genomics']: ") 

                if unit.upper() in bu_dict:
                    bu = bu_dict.get(unit)
                    #there is a class/file I need to create for this particular section
                    issues.mgmt_rp(bu)
                    user_input = input("Want to do something else? Admin Work [ 1 ], PR Checks [ 2 ], GitHub [ 3 ], exit [0]: ")
                else:
                    print("That's not an option")
        
            elif rp_answer.upper() == 'C':
                unit = input("Which business unit? ['ADD BU OPTIONS HERE]: ")
                if unit.lower() in bu_dict:
                    bu = bu_dict.get(unit)
                # Need a 
                    issues.dev_rp(bu)
                    user_input = input("Want to do something else?  Admin Work [ 1 ], PR Checks [ 2 ], GitHub [ 3 ], exit [0]: ")
                else:
                    print("That's not an option")
            else:
                print("That's not an option")                     

except Exception:
    print("Something went wrong.")
finally:
    print("Til Next Time")
