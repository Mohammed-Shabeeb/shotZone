import pandas as pd
from bs4 import BeautifulSoup
import os

def main():
    html_file_path = '../16_1_2025/in/buz.html'

    if not os.path.isfile(html_file_path):
        print(f"Error: The file {html_file_path} does not exist.")
        return

    try:
        # Opening HTML file with BeautifulSoup
        with open(html_file_path) as fp:
            innings_soup = BeautifulSoup(fp, "html.parser")

        # Create an empty dataframe
        ball_df = pd.DataFrame(columns=['ball', 'commentary'])

        # Create empty lists for each of the data you want
        ball_numbers = []
        ball_desc = []

        # Extract the relevant parent divs
        parent_divs = innings_soup.find_all('div', {'class': 'cb-col cb-col-100 ng-scope'})
        for parent_div in parent_divs:
            # Extract the ball number and commentary together from the corresponding divs
            ball_number_div = parent_div.find('div', {'class': 'cb-col cb-col-8 text-bold ng-scope'})
            ball_desc_p = parent_div.find('p')

            # Ensure that both ball number and description are present before adding to the list
            if ball_number_div and ball_desc_p:
                ball_numbers.append(ball_number_div.text.strip())
                ball_desc.append(ball_desc_p.text.strip())




        # Save lists in respective dataframe columns
        ball_df['ball'] = ball_numbers
        ball_df['commentary'] = ball_desc

        # Save dataframe as csv or json
        ball_df.to_csv("../16_1_2025/in/buz.csv", sep=',', index=False)
       # ball_df.to_json("Ball_by_Ball_Commentary_SL_vs_IND_1st_T20I.json", orient='records')

        print("Data has been successfully saved to CSV and JSON files.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    main()
