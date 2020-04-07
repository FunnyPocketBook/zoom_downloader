# Zoom-Downloader

## How to use
You need Python 3 for this. Download here https://www.python.org/downloads/

Install the required packages with 
```shell
pip install -r requirements.txt
```

There are two ways for using this script, using the CLI or using the `conf.json` file. When using the CLI, just add the links as arguments. Example:
```shell
python zoom-downloader.py "https://example.com" "https://example2.com" "https://example3.com" 
```

When using the `conf.json` file, add the URLs to the array.
```json
{
    "url": [
        "https://example.com",
        "https://example2.com",
        "https://example3.com"
    ],
    "workers": 5
}
```

The amount of workers for the thread pool can be also adjusted in `conf.json`.

## Output
The output is currently the root directory. I will add destination selection at some point in the future