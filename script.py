from subprocess import Popen
import os, requests
import people_also_ask as paa



try:
    os.remove("script2.py")
except:
    pass


try:
    query_file = open("query.txt","r")
    queries = query_file.readlines()
    query_file.close()

except:
    input("Query file is not in its location...")
    exit(1)
    

for query in queries:
    
    
    res_file = open("result.csv","a",encoding="utf_8")

    try:
        query = query.strip("\n")
    except Exception as e:
        print(e + str(1))

    print(f'Searching for "{query}"')
    try:
        questions = paa.get_related_questions(query ,14)
        try:

            queries.pop(queries.index(query))

        except:
            queries.pop(queries.index(query+"\n"))

    except:

        temp_query = open("query.txt","w")

        temp_query.writelines(queries)

        temp_query.close()

        script2 = open("script2.py","w")

        script2.writelines(["from subprocess import Popen\n","import time\n","time.sleep(2)\n","Popen('python script.py')\n","exit(0)"])
        
        Popen("python script2.py")

        exit(0)
        
    questions.insert(0,query)

    print("\n________________________\n")
    main_q = True
    for i in questions:
        if main_q:
            a = ""
            b = ""
            main_q = False
            first = True
            if i == query or i.split('?')[0] == query:
                print('same')
            else:
                res_file.write(str(f'{a}{query}?{b},"<p></p>",'))
        else:
            a = "<h2>"
            b = "</h2>"
        i = i.split('?')[0]

        try:
            print(f"Question:{i}?")
            answer = str(paa.get_answer(i)['response'])
            if answer[-1].isdigit():
                answer = answer[:-11]

            if "www.youtube.com" in answer or "https://youtu.be" in answer:
                try:
                    r = requests.get(f"https://www.youtube.com/oembed?url={answer}&format=json")
		            answer = r.json()['html']
                
                except Exception:
                    pass

                try:
                    answer = answer.replace(paa.get_answer(i)['displayed_link'],'')
                except KeyError:
                    pass

        except Exception:
            answer = ""
            print(f"Exception:{e}")
        if answer == "" and first == False:
            print('Skiping:\n\t No answer found')
            continue
        first = False
        print(f"Answer:{answer}")



        answer = answer.replace("\n","")
        res_file.write(str(f'{a}{i}?{b},"<p>{answer}</p>",'))

        print("______________________")

    print("______________________")
    res_file.write("\n")

    res_file.close()
try:
    os.remove("script2.py")
except:
    pass
print("\nSearch Complete.")
input("Press any key to Exit!")
