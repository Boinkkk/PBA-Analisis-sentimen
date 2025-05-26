from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

URL = "https://www.google.com/maps/place/RSUD+Syarifah+Ambami+Rato+Ebu/@-7.0293071,112.615115,12z/data=!4m10!1m2!2m1!1sRumah+sakit!3m6!1s0x2dd8057864d77839:0x73bf4e3ede9828a4!8m2!3d-7.0293071!4d112.7593106!15sCgtSdW1haCBzYWtpdFoNIgtydW1haCBzYWtpdJIBEGdlbmVyYWxfaG9zcGl0YWyqAU4KCC9tLzBocG5yEAEqDyILcnVtYWggc2FraXQoJjIeEAEiGpYnsAjHiAtC05DMrI_PR9YcL0KMEzP7xL8eMg8QAiILcnVtYWggc2FraXTgAQA!16s%2Fg%2F1hm2xn4n3?entry=ttu&g_ep=EgoyMDI1MDUyMS4wIKXMDSoJLDEwMjExNDUzSAFQAw%3D%3D"
iteration = 5 # -> Got around 1-5 data per iteration


def main():
    driver = webdriver.Chrome()

    driver.get(URL)

    # e_hospital = WebDriverWait(driver, 10).until(
    #     EC.visibility_of_element_located((By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[1]/div[1]/div[3]/div/a'))   Not Specific URL
    # )
    # e_hospital.click()

   
    ulasan_tab = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//button[contains(., 'Ulasan')]"))
    )


    driver.execute_script("arguments[0].scrollIntoView(true);", ulasan_tab)


    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Ulasan')]")))


    driver.execute_script("arguments[0].click();", ulasan_tab)

    element_tab = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[3]'))
    )

    for _ in range(iteration):
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollTop + 500;", element_tab)
        time.sleep(3)



    # driver.execute_script("arguments[0].scrollTop = arguments[0].scrollTop + 500;", element_tab)
    # time.sleep(3)                                                                                     Testing Perpose
    # driver.execute_script("arguments[0].scrollTop = arguments[0].scrollTop + 500;", element_tab)

        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "MyEned"))
        )


        print(f'Start Tacking Review')
        expand_buttons = driver.find_elements(By.XPATH, "//button[contains(., 'Lainnya')]")

        for btn in expand_buttons:
            try:
                driver.execute_script("arguments[0].click();", btn)
                time.sleep(0.5)
            except:
                continue

        review_spans = driver.find_elements(By.CSS_SELECTOR, "span.wiI7pd")
        reviews = [span.text for span in review_spans]

        for i, review in enumerate(reviews, 1):
            print(f"{i}. {review}")

        rating_spans = driver.find_elements(By.CSS_SELECTOR, "span.kvMYJc")

        ratings = []
        for span in rating_spans:
            aria_label = span.get_attribute("aria-label")
            if aria_label:
                try:
                    bintang = int(aria_label.split()[0])  
                    ratings.append(bintang)
                except:
                    ratings.append(None)
            else:
                ratings.append(None)

        for i, rating in enumerate(ratings, 1):
            print(f"Review {i}: {rating} bintang")

    print(reviews)
    print(ratings)

    sentimen_list = list(zip(ratings,reviews))

    with open("output.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Rating", "Review"])  # Header
        writer.writerows(sentimen_list)


    print(f'Done Tacking Review')



   

    driver.close()


if __name__ == '__main__':
    main()


