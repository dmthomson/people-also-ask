from subprocess import Popen
import os, requests
from os.path import exists
import people_also_ask as paa


def remove_files(temp_file: str) -> None:
    try:
        file_exists = exists(temp_file)

        if file_exists:
            print(f"Removing existing file {file_exists}")
            os.remove(temp_file)

    except FileExistsError as e:
        print(f"Error Message: {e}")
        exit(1)


def get_queries_from_file(query_file: str) -> list:
    try:
        with open(query_file, "r") as query_file:
            queries = query_file.readlines()
            print(queries)
            return queries

    except FileNotFoundError as e:
        print(f"Error Message: {e}")
        exit(1)


print("Made it passed this point")


def search_queries(queries: list) -> None:
    print(queries)
    for query in queries:
        with open("result.csv", "a", encoding="utf_8") as res_file:
            try:
                query = query.strip("\n")
            except Exception as e:
                print(e + str(1))

                print(f'Searching for "{query}"')
            try:
                questions = paa.get_related_questions(query, 14)
                try:
                    queries.pop(queries.index(query))

                except Exception:
                    queries.pop(queries.index(query + "\n"))

            except Exception:

                temp_query = open("query.txt", "w")

                temp_query.writelines(queries)

                temp_query.close()

                with open("script2.py", "w") as script2:

                    script2.writelines(
                        [
                            "from subprocess import Popen\n",
                            "import time\n",
                            "time.sleep(2)\n",
                            "Popen('python main.py')\n",
                            "exit(0)",
                        ]
                    )

                Popen("python script2.py")

                exit(0)

            questions.insert(0, query)

            print("\n________________________\n")
            main_q = True
            for i in questions:
                if main_q:
                    a = ""
                    b = ""
                    main_q = False
                    first = True
                    if i == query or i.split("?")[0] == query:
                        print("same")
                    else:
                        res_file.write(str(f'{a}{query}?{b},"<p></p>",'))
                else:
                    a = "<h2>"
                    b = "</h2>"
                i = i.split("?")[0]

                try:
                    print(f"Question:{i}?")
                    answer = str(paa.get_answer(i)["response"])
                    if answer[-1].isdigit():
                        answer = answer[:-11]

                    if "www.youtube.com" in answer or "https://youtu.be" in answer:
                        try:
                            r = requests.get(
                                f"https://www.youtube.com/oembed?url={answer}&format=json"
                            )
                            answer = r.json()["html"]

                        except Exception:
                            pass

                        try:
                            answer = answer.replace(
                                paa.get_answer(i)["displayed_link"], ""
                            )
                        except KeyError:
                            pass

                except Exception as e:
                    answer = ""
                    print(f"Exception:{e}")

                if answer == "" and first == False:
                    print("Skipping:\n\t No answer found")
                    continue
                first = False
                print(f"Answer:{answer}")

                answer = answer.replace("\n", "")
                res_file.write(str(f'{a}{i}?{b},"<p>{answer}</p>",'))

                print("______________________")

            print("______________________")

    print("\nSearch Complete.")
    input("Press any key to Exit!")


def main():
    temp_file = "./script2"
    query_file = "query.txt"

    remove_files(temp_file)
    queries = get_queries_from_file(query_file)
    search_queries(queries)
    remove_files(temp_file)


if __name__ == "__main__":
    main()
