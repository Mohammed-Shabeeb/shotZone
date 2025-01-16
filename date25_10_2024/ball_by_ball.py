import pandas as pd
from bs4 import BeautifulSoup

def main():
    # Opening HTML file with BeautifulSoup
    with open('../16_1_2025/in/info.html') as fp:
        innings_soup = BeautifulSoup(fp, "html.parser")

    # Create an empty dataframe
    ball_df = pd.DataFrame(columns=['ball', 'score', 'commentary'])

    # Create empty lists for each of the data you want
    ball_numbers = []
    ball_scores = []
    ball_desc = []

    # Define a list of possible div classes for scores
    score_div_classes = [
        'ds-flex ds-items-center ds-justify-center ds-rounded ds-overflow-hidden ds-bg-ui-fill-default-translucent ds-text-typo',
        'ds-flex ds-items-center ds-justify-center ds-rounded ds-overflow-hidden ds-bg-raw-green-d2 ds-text-raw-white',
        'ds-flex ds-items-center ds-justify-center ds-rounded ds-overflow-hidden ds-bg-raw-purple ds-text-raw-white',
        'ds-flex ds-items-center ds-justify-center ds-rounded ds-overflow-hidden ds-bg-raw-red ds-text-raw-white'
    ]

    # Extract ball numbers and scores
    for div in innings_soup.findAll('div', {'class': 'lg:ds-flex lg:ds-items-center lg:ds-px-2'}):
        # Extract ball number
        ball_number = div.find('span', {'class': 'ds-text-tight-s ds-font-regular ds-mb-1 lg:ds-mb-0 lg:ds-mr-3 ds-block ds-text-center ds-text-typo-mid1'})
        if ball_number:
            ball_numbers.append(ball_number.text.strip())

        # Extract score on each ball
        score = ''
        for cls in score_div_classes:
            score_div = div.find('div', {'class': cls})
            if score_div:
                score = score_div.text.strip()
                break
        
        ball_scores.append(score)

    # Extract description for each ball
    # for div in innings_soup.findAll('div', {'class': 'xl:ds-w-[730px]'}):
    #     ball_desc.append(div.text.strip())
    # Extract description for each ball
    for div in innings_soup.findAll('div', {'class': 'xl:ds-w-[730px]'}):
        # Initialize an empty list for the description parts
        description_parts = []

        # Collect the text from the relevant tags
        for tag in div.find_all(['span', 'p']):  # Adjust the tags as necessary
            # Append the text while stripping and ensuring spaces
            description_parts.append(tag.text.strip())

        # Join all parts with a space
        description = ' '.join(description_parts)
        ball_desc.append(description)

    # Ensure that all lists have the same length
    min_len = min(len(ball_numbers), len(ball_scores), len(ball_desc))
    ball_numbers = ball_numbers[:min_len]
    ball_scores = ball_scores[:min_len]
    ball_desc = ball_desc[:min_len]

    # Save lists in respective dataframe columns
    ball_df['ball'] = ball_numbers
    ball_df['score'] = ball_scores
    ball_df['commentary'] = ball_desc

    # Save dataframe as csv or json
    ball_df.to_csv("../16_1_2025/in/info.csv", sep=',', index=False)
    # ball_df.to_json("Ball by Ball Commentary & Live Score - SL vs IND, 1st T20I_1.json", orient='records')

if __name__ == '__main__':
    main()
