import json
import pandas as pd
from searchtweets import load_credentials, gen_rule_payload, ResultStream
import yaml

# save credentials to yaml file (Rastogi, 2020)
config = dict(
    search_tweets_api=dict(
        account_type='premium',
        endpoint='https://api.twitter.com/1.1/tweets/search/fullarchive/NAME.json',
        consumer_key='CONSUMER KEY',
        consumer_secret='CONSUMER SECRET'
    )
)
with open('twitterkeys.yaml', 'w') as config_file:
    yaml.dump(config, config_file, default_flow_style=False)

# load credentials and create bearer token (Rastogi, 2020; Hammar, 2019)
premium_search_args = load_credentials("twitterkeys.yaml",
                                       yaml_key="search_tweets_api",
                                       env_overwrite=False)
print(premium_search_args)

# search rule (Rastogi, 2020; GitHub, 2020; Hammar, 2019)
rule = gen_rule_payload("KEYWORD",
                        results_per_call = 100,
                        from_date = 'YYYY-MM-DD',
                        to_date = 'YYYY-MM-DD'
                        )

rs = ResultStream(rule_payload=rule,
                  max_results=100,
                  **premium_search_args)
print(rule)
print(rs)

# save results to json file (Rastogi, 2020; Hammar, 2019)
with open('FILE.json', 'a', encoding='utf-8') as f:
    for tweet in rs.stream():
        json.dump(tweet, f)
        f.write('\n')

# convert json file to csv (Gregory, 2020)
df = pd.read_json('FILE.json', lines=True)
df.to_csv('FILE.csv')
print('done')