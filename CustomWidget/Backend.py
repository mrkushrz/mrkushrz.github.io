{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/mrkushrz/mrkushrz.github.io/blob/main/CustomWidget/Backend.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "!pip install openai"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "XkzOtqWkE9qN",
        "outputId": "0c159e4a-d70a-4510-f162-ed63bf170abc"
      },
      "execution_count": 1,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Requirement already satisfied: openai in /usr/local/lib/python3.10/dist-packages (1.3.7)\n",
            "Requirement already satisfied: anyio<4,>=3.5.0 in /usr/local/lib/python3.10/dist-packages (from openai) (3.7.1)\n",
            "Requirement already satisfied: distro<2,>=1.7.0 in /usr/lib/python3/dist-packages (from openai) (1.7.0)\n",
            "Requirement already satisfied: httpx<1,>=0.23.0 in /usr/local/lib/python3.10/dist-packages (from openai) (0.25.2)\n",
            "Requirement already satisfied: pydantic<3,>=1.9.0 in /usr/local/lib/python3.10/dist-packages (from openai) (1.10.13)\n",
            "Requirement already satisfied: sniffio in /usr/local/lib/python3.10/dist-packages (from openai) (1.3.0)\n",
            "Requirement already satisfied: tqdm>4 in /usr/local/lib/python3.10/dist-packages (from openai) (4.66.1)\n",
            "Requirement already satisfied: typing-extensions<5,>=4.5 in /usr/local/lib/python3.10/dist-packages (from openai) (4.5.0)\n",
            "Requirement already satisfied: idna>=2.8 in /usr/local/lib/python3.10/dist-packages (from anyio<4,>=3.5.0->openai) (3.6)\n",
            "Requirement already satisfied: exceptiongroup in /usr/local/lib/python3.10/dist-packages (from anyio<4,>=3.5.0->openai) (1.2.0)\n",
            "Requirement already satisfied: certifi in /usr/local/lib/python3.10/dist-packages (from httpx<1,>=0.23.0->openai) (2023.11.17)\n",
            "Requirement already satisfied: httpcore==1.* in /usr/local/lib/python3.10/dist-packages (from httpx<1,>=0.23.0->openai) (1.0.2)\n",
            "Requirement already satisfied: h11<0.15,>=0.13 in /usr/local/lib/python3.10/dist-packages (from httpcore==1.*->httpx<1,>=0.23.0->openai) (0.14.0)\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "import os\n",
        "from openai import AzureOpenAI"
      ],
      "metadata": {
        "id": "EO2ifNAbCKgU"
      },
      "execution_count": 2,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "os.environ['AZURE_OPENAI_KEY'] = '65ee6d36768e44b894d04c922e6cbe7a'\n",
        "os.environ['AZURE_OPENAI_ENDPOINT'] = 'https://mbeopenai.openai.azure.com/'\n",
        "\n",
        "client = AzureOpenAI(\n",
        "  api_key = os.getenv(\"AZURE_OPENAI_KEY\"),\n",
        "  api_version = \"2023-05-15\",\n",
        "  azure_endpoint = os.getenv(\"AZURE_OPENAI_ENDPOINT\")\n",
        ")"
      ],
      "metadata": {
        "id": "fd2nE_RBCMyS"
      },
      "execution_count": 3,
      "outputs": []
    },
    {
      "cell_type": "code",
      "execution_count": 4,
      "metadata": {
        "id": "IfPIZ16YbsIb"
      },
      "outputs": [],
      "source": [
        "import requests\n",
        "from bs4 import BeautifulSoup\n",
        "import pandas as pd\n",
        "from datetime import datetime, timedelta\n",
        "import yfinance as yf\n",
        "import re"
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "def get_commodity_profile(commodity_name):\n",
        "    prompt = f\"Generate a short description for the commodity {commodity_name} (e.g., sugar, wheat). Also list general positive and negative factors that might impact its price. Be brief and use keywords. Consider diverse factors including agricultural production conditions (e.g., weather patterns, crop yield), market dynamics (e.g., global supply and demand, stock levels), economic factors (e.g., inflation, trade policies), and environmental considerations (e.g., sustainability, climate change). Use the format Description: ..., Positive Factors: ..., Negative Factors: ...\"\n",
        "\n",
        "    response = client.chat.completions.create(\n",
        "        model=\"GPT35\",\n",
        "        messages=[ #Verbesserungen möglich\n",
        "            {\"role\": \"system\", \"content\": \"Assistant is a large language model trained by OpenAI.\"},\n",
        "            {\"role\": \"user\", \"content\": prompt}\n",
        "        ]\n",
        "    )\n",
        "    return response.choices[0].message.content"
      ],
      "metadata": {
        "id": "pSoF_QIYbIzV"
      },
      "execution_count": 5,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "def format_market_data(df):\n",
        "    df.reset_index(inplace=True)\n",
        "    df['Date'] = df['Date'].dt.strftime('%m/%d/%Y')\n",
        "    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')\n",
        "    df.set_index('Date', inplace=True)\n",
        "    return df"
      ],
      "metadata": {
        "id": "eT82UPAAHcJr"
      },
      "execution_count": 6,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "# Dictionary to store data frames and their sources for each commodity\n",
        "commodity_data = {}\n",
        "\n",
        "# Fetch and process data for US Sugar #11 Futures\n",
        "sbf = yf.Ticker(\"SB=F\")\n",
        "hist_sugar11 = sbf.history(period=\"max\")\n",
        "df_sugar11 = pd.DataFrame(hist_sugar11).drop(columns=['Dividends', 'Stock Splits'])\n",
        "df_sugar11 = format_market_data(df_sugar11)\n",
        "commodity_data[\"globalsugar\"] = {\"data\": df_sugar11, \"source\": \"SB=F\"}\n",
        "\n",
        "# Add more commodities in a similar way\n",
        "# Example for European Sugar (Placeholder Tickers)\n",
        "# sbf_euro = yf.Ticker(\"EURO_SUGAR_TICKER\")\n",
        "# hist_eurosugar = sbf_euro.history(period=\"max\")\n",
        "# df_eurosugar = pd.DataFrame(hist_eurosugar).drop(columns=['Dividends', 'Stock Splits'])\n",
        "# df_eurosugar = format_market_data(df_eurosugar)\n",
        "# commodity_data[\"europeansugar\"] = {\"data\": df_eurosugar, \"source\": \"EURO_SUGAR_TICKER\"}\n",
        "\n",
        "# If European Sugar requires data from multiple sources, merge them\n",
        "# df_combined_eurosugar = pd.concat([df_eurosugar, df_other_source])\n",
        "# commodity_data[\"europeansugar\"] = {\"data\": df_combined_eurosugar, \"source\": [\"EURO_SUGAR_TICKER\", \"OTHER_SOURCE_TICKER\"]}"
      ],
      "metadata": {
        "id": "AROL5ookHOZ-"
      },
      "execution_count": 7,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "def get_price_data(commodity_name, start_date, end_date):\n",
        "    commodity_info = commodity_data.get(commodity_name)\n",
        "    if commodity_info is None:\n",
        "        raise ValueError(f\"No data available for commodity: {commodity_name}\")\n",
        "\n",
        "    df = commodity_info[\"data\"]\n",
        "    start_date_dt = pd.to_datetime(start_date)\n",
        "    three_weeks_before = start_date_dt - timedelta(weeks=3)\n",
        "    end_date_dt = pd.to_datetime(end_date)\n",
        "    filtered_data = df.loc[three_weeks_before:end_date_dt]\n",
        "\n",
        "    return filtered_data, commodity_info[\"source\"]"
      ],
      "metadata": {
        "id": "OeP3XWw6HaqK"
      },
      "execution_count": 8,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "def format_price_data_sources(commodity_name, start_date, end_date):\n",
        "    # Access commodity data and handle the case where there's no data\n",
        "    commodity_sources = commodity_data.get(commodity_name, [])\n",
        "    if not commodity_sources:\n",
        "        raise ValueError(f\"No data available for commodity: {commodity_name}\")\n",
        "\n",
        "    # Initialize variable for formatted source and price data\n",
        "    formatted_data = \"\"\n",
        "\n",
        "    if isinstance(commodity_sources, dict):  # Handle single source\n",
        "      commodity_sources = [commodity_sources]\n",
        "\n",
        "    # Loop over each source and get and format its data\n",
        "    for source_info in commodity_sources: # Multiple Source\n",
        "        # Get filtered data for each source\n",
        "        filtered_data, _ = get_price_data(commodity_name, start_date, end_date)\n",
        "\n",
        "        # Append formatted data for each source\n",
        "        formatted_data += f\"(Source/Ticker: {source_info['source']}):\\n{filtered_data}\\n\\n\"\n",
        "\n",
        "    return formatted_data"
      ],
      "metadata": {
        "id": "0yROXC1I3drs"
      },
      "execution_count": 9,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "def generate_analysis_prompt(commodity_name, start_date, end_date, commodity_profile, df_news):\n",
        "\n",
        "    price_data = format_price_data_sources(commodity_name, start_date, end_date)\n",
        "\n",
        "    news = []  # Initialize an empty list\n",
        "\n",
        "    for index, row in df_news.iterrows():\n",
        "      news.append(row['summary_and_keywords']+ '\\n')\n",
        "\n",
        "    prompt = f\"\"\"\n",
        "    Instruction: Explain the price movement for the commodity {commodity_name} from {start_date} to {end_date}, by analyzing the commodity's market profile, historical weekly news summary, keywords, and price history. Discuss the factors that influenced the price movement.\n",
        "\n",
        "    Commodity Profile: {commodity_profile}\n",
        "    Price History:\n",
        "    {price_data}\n",
        "    Recent News: News are ordered weekly from oldest to latest.\n",
        "    {news}\n",
        "\n",
        "    Now analyze the commodity's price movement from {start_date} to {end_date}. Only use the prices provided.\n",
        "    Provide a Summary and an analysis of the Commodity Price Movement.\n",
        "    The analysis should comprehensively explain the reasons, key factors and events that influenced the price movement.\n",
        "    Do not just summarize the history. Reason step by step before the finalized output.\n",
        "    Use format Summary: ..., Commodity Price Movement Analysis: ...\n",
        "    Use bulletpoints for structuring the different factors and events in the analysis.\n",
        "    \"\"\"\n",
        "\n",
        "    return prompt"
      ],
      "metadata": {
        "id": "Ef_VpyLL5-Pr"
      },
      "execution_count": 10,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "def generate_forecast_prompt(commodity_name, start_date, end_date, commodity_profile, df_news):\n",
        "\n",
        "    price_data = format_price_data_sources(commodity_name, start_date, end_date)\n",
        "\n",
        "    news = []  # Initialize an empty list\n",
        "\n",
        "    for index, row in df_news.iterrows():\n",
        "      news.append(row['summary_and_keywords']+ '\\n')\n",
        "\n",
        "    prompt = f\"\"\"\n",
        "    Instruction: Forecast next month's price movement for the commodity {commodity_name}, given the commodity's market profile, historical weekly news summary, keywords, and price trends, and optionally examples from similar commodities.\n",
        "\n",
        "    The trend is represented by bins \"D5+\", \"D5\", \"D4\", \"D3\", \"D2\", \"D1\", \"U1\", \"U2\", \"U3\", \"U4\", \"U5\", \"U5+\", where \"D5+\" means price dropping more than 5%, D5 means price dropping between 4% and 5%, and so on, with \"U\" indicating upward trends and “D” indication downward trends.\n",
        "\n",
        "    Commodity Profile: {commodity_profile}\n",
        "\n",
        "    Prices\n",
        "    {price_data}\n",
        "    Recent Commodity News: News are ordered weekly from oldest to latest.\n",
        "    {news}\n",
        "\n",
        "\n",
        "    Now predict what could be the next month’s Summary, Keywords, and forecast the Commodity Price Movement.\n",
        "    The predicted Summary/Keywords should explain the price movement forecasting.\n",
        "    You should predict what could happen next month/s. Do not just summarize the history.\n",
        "    The next month's price movement must not be the same as the previous weeks.\n",
        "    Reason step by step before the finalized output.\n",
        "    Use format Summary: ..., Commodity Price Movement: ...\n",
        "    \"\"\"\n",
        "\n",
        "    return prompt"
      ],
      "metadata": {
        "id": "8xvZ3ucn_Xlh"
      },
      "execution_count": 11,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "import sqlite3\n",
        "\n",
        "def fetch_news_data(db_path):\n",
        "    \"\"\"\n",
        "    Connects to an SQLite database, fetches all data from the news_table,\n",
        "    and returns it as a pandas DataFrame.\n",
        "\n",
        "    Parameters:\n",
        "    db_path (str): Path to the SQLite database file.\n",
        "\n",
        "    Returns:\n",
        "    pd.DataFrame: DataFrame containing the fetched news data.\n",
        "    \"\"\"\n",
        "    # Connect to the SQLite database\n",
        "    connection = sqlite3.connect(db_path)\n",
        "\n",
        "    # Create a cursor object\n",
        "    cursor = connection.cursor()\n",
        "\n",
        "    # Execute a query to fetch all data from the news_table\n",
        "    cursor.execute(\"SELECT * FROM news_table\")\n",
        "\n",
        "    # Fetch all rows from the query\n",
        "    rows = cursor.fetchall()\n",
        "\n",
        "    # Convert the rows to a DataFrame\n",
        "    df_news = pd.DataFrame(rows, columns=[description[0] for description in cursor.description])\n",
        "\n",
        "    # Close the connection to the database\n",
        "    connection.close()\n",
        "\n",
        "    # Convert the 'timedate' column to datetime and format it\n",
        "    df_news['timedate'] = pd.to_datetime(df_news['timedate']).dt.strftime('%m/%d/%Y')\n",
        "\n",
        "    return df_news"
      ],
      "metadata": {
        "id": "tL9TKnak-sRx"
      },
      "execution_count": 12,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "def filter_dataframe_by_date(df, start_date, end_date):\n",
        "\n",
        "    # Convert the start and end dates to datetime\n",
        "    start_date = pd.to_datetime(start_date)\n",
        "    end_date = pd.to_datetime(end_date)\n",
        "\n",
        "    # Calculate the date 3 weeks before the start date\n",
        "    start_date_minus_3_weeks = start_date - timedelta(weeks=3)\n",
        "\n",
        "    # Filter the dataframe\n",
        "    filtered_df = df[(pd.to_datetime(df['timedate']) >= start_date_minus_3_weeks) & (pd.to_datetime(df['timedate']) <= end_date)]\n",
        "\n",
        "    return filtered_df"
      ],
      "metadata": {
        "id": "2HoE33EgFAfu"
      },
      "execution_count": 13,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "def generate_commodity_response(start_date, end_date, commodity, prompt):\n",
        "    df_news = fetch_news_data('news_data_2023.db')\n",
        "    df_news = filter_dataframe_by_date(df_news, start_date, end_date)  # Replace df_news with a call to your SQLite database\n",
        "\n",
        "    commodity_profile = get_commodity_profile(commodity)\n",
        "\n",
        "    if prompt == \"analysis\":\n",
        "        generated_prompt = generate_analysis_prompt(commodity, start_date, end_date, commodity_profile, df_news)\n",
        "    elif prompt == \"forecast\":\n",
        "        generated_prompt = generate_forecast_prompt(commodity, start_date, end_date, commodity_profile, df_news)\n",
        "    else:\n",
        "        raise ValueError(\"Invalid prompt type. Choose 'analysis' or 'forecast'.\")\n",
        "\n",
        "    response = client.chat.completions.create(\n",
        "        model=\"GPT35\",\n",
        "        messages=[\n",
        "            {\"role\": \"system\", \"content\": \"Forget all your previous instructions. Pretend you are a commodity market analyst. You are a financial expert with experience in analyzing, interpreting and forecasting commodity market trends, specifically focusing on commodities like sugar or wheat.\"},\n",
        "            {\"role\": \"user\", \"content\": generated_prompt}\n",
        "        ]\n",
        "    )\n",
        "\n",
        "\n",
        "    return response.choices[0].message.content"
      ],
      "metadata": {
        "id": "h8piqk866E34"
      },
      "execution_count": 18,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "print(generate_commodity_response('03/19/2023', '04/24/2023', 'globalsugar', 'analysis'))"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 1000
        },
        "id": "GjHBrSE2w5-q",
        "outputId": "a9ec3569-ef2a-4530-8b87-7753e956ec9f"
      },
      "execution_count": 19,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "\n",
            "    Instruction: Explain the price movement for the commodity globalsugar from 03/19/2023 to 04/24/2023, by analyzing the commodity's market profile, historical weekly news summary, keywords, and price history. Discuss the factors that influenced the price movement.\n",
            "\n",
            "    Commodity Profile: Description: Global sugar refers to the commodity of sucrose that is traded globally. It is primarily produced from sugarcane and sugar beet.\n",
            "\n",
            "Positive Factors:  Good weather conditions, higher crop yields, increasing global demand, low stock levels, government subsidies, favorable trade policies, and sustainable production practices can all lead to higher sugar prices.\n",
            "\n",
            "Negative Factors: Adverse weather conditions, lower crop yields, decreasing global demand, high stock levels, reduction or removal of government subsidies, unfavorable trade policies, and climate change leading to unpredictable production conditions can all lead to lower sugar prices. Additionally, concerns over the health impacts of consuming large amounts of sugar can also impact demand and price.\n",
            "    Price History:\n",
            "    (Source/Ticker: SB=F):\n",
            "                 Open       High        Low      Close  Volume\n",
            "Date                                                          \n",
            "2023-02-27  21.370001  22.139999  21.270000  22.090000   14804\n",
            "2023-02-28  22.110001  22.360001  22.000000  22.080000   52032\n",
            "2023-03-01  20.090000  20.650000  20.040001  20.570000   63125\n",
            "2023-03-02  20.570000  20.620001  20.200001  20.309999   45550\n",
            "2023-03-03  20.350000  21.040001  20.320000  20.920000   80261\n",
            "2023-03-06  20.930000  20.959999  20.629999  20.870001   52864\n",
            "2023-03-07  20.870001  21.250000  20.809999  21.020000   61931\n",
            "2023-03-08  21.000000  21.030001  20.770000  20.879999   49057\n",
            "2023-03-09  20.820000  21.330000  20.709999  21.150000   65365\n",
            "2023-03-10  21.040001  21.219999  20.660000  21.160000   68291\n",
            "2023-03-13  21.230000  21.270000  20.700001  20.799999   86999\n",
            "2023-03-14  20.860001  21.020000  20.650000  20.680000   58309\n",
            "2023-03-15  20.639999  20.700001  20.389999  20.500000   65626\n",
            "2023-03-16  20.610001  20.850000  20.350000  20.760000   62707\n",
            "2023-03-17  20.790001  20.940001  20.530001  20.670000   39076\n",
            "2023-03-20  20.500000  20.690001  20.420000  20.480000   38677\n",
            "2023-03-21  20.600000  20.920000  20.490000  20.799999   36603\n",
            "2023-03-22  20.850000  21.379999  20.780001  21.139999   55324\n",
            "2023-03-23  21.150000  21.340000  20.809999  20.889999   55228\n",
            "2023-03-24  20.969999  20.990000  20.650000  20.820000   54542\n",
            "2023-03-27  20.910000  21.150000  20.740000  20.930000   46275\n",
            "2023-03-28  20.990000  21.450001  20.959999  21.309999   52748\n",
            "2023-03-29  21.379999  21.420000  21.049999  21.250000  102713\n",
            "2023-03-30  21.299999  22.000000  21.299999  21.959999  116898\n",
            "2023-03-31  21.990000  22.360001  21.780001  22.250000   77059\n",
            "2023-04-03  22.350000  22.629999  22.190001  22.400000   87499\n",
            "2023-04-04  22.250000  22.600000  22.219999  22.469999   71132\n",
            "2023-04-05  22.480000  23.010000  22.410000  22.950001  112569\n",
            "2023-04-06  23.010000  23.680000  22.709999  23.610001       0\n",
            "2023-04-10  23.559999  23.820000  23.440001  23.559999  112764\n",
            "2023-04-11  23.730000  24.450001  23.620001  24.370001  169537\n",
            "2023-04-12  24.650000  24.850000  23.920000  24.049999  115222\n",
            "2023-04-13  24.000000  24.700001  23.900000  24.040001   71323\n",
            "2023-04-14  23.920000  24.270000  23.750000  24.100000   53482\n",
            "2023-04-17  24.250000  24.500000  24.120001  24.440001   58060\n",
            "2023-04-18  24.440001  24.690001  24.100000  24.540001   48827\n",
            "2023-04-19  24.459999  24.900000  24.299999  24.370001   34138\n",
            "2023-04-20  24.260000  25.370001  24.190001  25.250000   37220\n",
            "2023-04-21  25.620001  25.620001  24.670000  24.830000   39739\n",
            "2023-04-24  24.770000  25.990000  24.600000  25.910000   46336\n",
            "\n",
            "\n",
            "    Recent News: News are ordered weekly from oldest to latest.\n",
            "    ['Summary: A study has linked erythritol, a sugar replacement commonly used in reduced-sugar products, to an increased risk of blood clotting, stroke, heart attack, and death. People with existing risk factors for heart disease such as diabetes were twice as likely to experience a heart attack or stroke if they had the highest levels of erythritol in their blood. The discovery of the connection between erythritol and cardiovascular issues was accidental, and the results indicate that more research is needed to determine the safety of the widely available product. \\n\\nKeywords: erythritol, sugar replacement, blood clotting, stroke, heart attack, cardiovascular issues, diabetes, research, safety.\\n', 'Summary: As consumers become more health-conscious, the beverage industry is turning to natural, plant-based sweeteners like stevia, erythritol, monk fruit, and allulose to create low-sugar or sugar-free drinks that still taste great. Consumers want clean label attributes and recognizable ingredients, leading to an increase in demand for natural sweeteners. A combination of sweeteners is often used to address mouthfeel and off-notes, and many plant-derived sweeteners are used to achieve a desired flavor and sweetness profile. Consumers also want beverages with additional health benefits, fueling the growth of naturally sweet, zero-calorie beverages. \\n\\nKeywords: beverage industry, natural sweeteners, plant-based, low-sugar, stevia, monk fruit, erythritol, allulose, clean label, mouthfeel, off-notes, health benefits, zero-calorie.\\n', \"Summary: Al Khaleej Sugar in Dubai is operating at 40% capacity due to India's dumping of sugar, according to the company's Managing Director. Other countries have complained that India has violated WTO rules related to subsidies for sugar and sugarcane. India has appealed a WTO panel's ruling against them. The lower capacity has impacted Al Khaleej Sugar's expansion plans. The European Commission has included energy initiatives from Italy's Snam, Eni, and Terna in a list of Projects of Common Interest.\\n\\nKeywords: Al Khaleej Sugar, Dubai, India, dumping, WTO, subsidies, sugar, sugarcane, appeals, lower capacity, expansion plans, European Commission, Snam, Eni, Terna, energy initiatives, Projects of Common Interest.\\n\", \"Summary: The French sugar beet crop area is expected to fall to a 14-year low this year despite high prices, with farmers deterred by potential crop damage because of pesticide restrictions. French farmers have suffered poor harvests in recent years due to jaundice disease and summer drought. Concern over possible crop damage this year has increased after an EU court last month overturned French policy allowing sugar beet growers another year's use of an insecticide banned by the bloc. Keywords: French sugar beet crop, low crop area, high prices, potential crop damage, pesticide restrictions, poor harvests, jaundice disease, drought, EU court, insecticide ban.\\n\", \"Summary: Analysts are predicting a global sugar surplus in 2022-23, and lower production in some key countries such as India may offset declines in the current marketing year. However, forecasts of higher production in Brazil in 2023-24 are expected to offset some of these declines. Despite the surplus, analysts expect sugar prices to remain elevated but not necessarily at current six- or seven-year highs. Thailand is expected to increase sugar production, but the current production outlook is viewed more as a bounce back rather than a trend upwards. A mild winter followed by extremely hot and dry summer conditions created a stressful environment for the European Union's crop, and the situation was further exacerbated by a scourge of beet yellow virus, likely linked to the EU’s recent ban on neonicotinoid insecticides, which have been blamed for killing bees. The late January ransomware attack on the Dublin-based ION Cleared Derivatives digital trading platform also impacted the global sugar outlook. \\n\\nKeywords: sugar surplus, global sugar market, production declines, Brazil, India, sugar prices, Thailand, EU crop, beet yellow virus, ION Cleared Derivatives.\\n\", \"Summary: White sugar futures rose for a third day due to mounting supply concerns, with the premium for refined sugar over raw sweetener reaching a six-month high. Crop issues in several regions have led to downward supply revisions, and buyers are facing difficulties in stockpiling. Brazilian supplies may not bring much relief to the refined sugar market as the country's production of refined sugar is small.\\n\\nKeywords: White sugar futures, supply concerns, premium, refined sugar, raw sweetener, crop issues, supply revisions, stockpiling, Brazilian supplies\\n\", 'Summary: The news might be related to the Indian elections, technology, and economy in 2023, as per the available information. \\n\\nKeywords: Bloomberg, India, Elections 2023, Technology News, Economy News.\\n', 'Summary: The price of sugar is increasing and this is putting pressure on global food inflation. The surge in refined sugar prices is the highest for a month since 2021, and the raw sugar variety is near its most expensive level in over six years. The limited global supply is due to India cutting sugar exports after their crops were hit by bad weather and more sugar is being used to make biofuel.\\n\\nKeywords: sugar, price increase, global food inflation, refined sugar, raw sugar, India, limited supply, bad weather, biofuel.\\n', 'Summary: Sugar company stocks have surged due to hopes of an increase in retail prices of sugar following a global trend and strong demand for ethanol. The sugar production in India has increased by 2.8% till February 15th of this financial year, and the government plans to allow an addition of one million tonnes of sugar if the domestic sugar production reaches its estimate of 336 lakh tonne. The government is planning to create a buffer of ethanol stock for the next year in anticipation of a rise in E20 fuel which is a blend of ethanol with petrol. Keywords: Sugar company stocks, global trend, ethanol, sugar production, India, government, ethanol blending, E20 fuel, petrol\\n', 'Summary: MSM Malaysia Holdings Bhd is expected to incur losses in the first half of 2023 due to the lack of clarity on its proposal to change retail sugar prices and the inability to increase utilization rates of its refinery in Johor. The rising global raw sugar prices are expected to further impact its profit margins, especially for its domestic wholesale segment. The company\\'s fundraising plans may dilute its earnings per share if it involves a share placement exercise. The group is planning to raise funds through share placements or a rights issue to reduce its debt. CGS-CIMB Research has reiterated a \"reduce\" rating on the stock with a target price of 58 sen. \\nKeywords: MSM Malaysia Holdings Bhd, losses, first half 2023, retail sugar prices, refinery, Johor, global raw sugar prices, profit margins, fundraising plans, share placements, rights issue, debt reduction, CGS-CIMB Research.\\n', 'Summary: Tereos, France’s largest ethanol and sugar group, is restructuring its facilities due to a decline in sugar beet yields and to adapt to decarbonization efforts. As a result, the company plans to cease sugar operations at Escaudoeuvres, one of its sugar processing factories in northern France, and is seeking a buyer for its potato starch mill in Haussimont, eastern France. Tereos is also redeploying employees affected by the reorganization to other positions within Tereos. Rising energy costs have been another factor in the reorganization effort.\\n\\nKeywords: Tereos, France, sugar, sugar beet, environmental factors, decarbonization, restructuring, factory closure, potato starch mill, reorganization, energy costs.\\n', 'Summary: N/A, \\nKeywords: notifications, article.\\n', 'Summary: Sugar consumption can cause dental problems, obesity, diabetes, inflammation, and an increased risk of heart disease. People are consuming greater amounts of sugar than ever, particularly in the form of sugar-laden beverages. This has led to a booming market in artificial sweeteners. However, studies about whether artificial sweeteners might also have adverse health effects are inconclusive. Recently, one popular sugar substitute, erythritol, has been associated with an increased risk of heart attack, stroke, and blood clots. Nevertheless, correlation is not causation, and more study is needed. Three-quarters of Americans eat more sugar than they should, and experts recommend consuming less sugar and artificial sweeteners. Sugar-sweetened beverages don’t satisfy hunger, and using artificial sweeteners can actually lead to weight gain by increasing appetite and sugar cravings. \\n\\nKeywords: sugar, dental problems, obesity, diabetes, inflammation, heart disease, artificial sweeteners, erythritol, studies, health effects, Americans, sugar consumption, weight gain.\\n', 'Summary: N/A\\nKeywords: enable, JS, disable, ad blocker.\\n', 'N/A\\n', 'Summary: The global beet sugar market is expected to reach USD 5.8 Billion by 2030 at a CAGR of 5.3% over the forecast period 2023-2030. The rising demand for natural sweeteners, the increasing use of beetroot juice extract as a natural and viable source of nutrients in energy beverages, and the growth of artisan beets as a superior substitute for extract sweeteners are expected to drive market growth. The Asia Pacific region is expected to be the fastest-growing region in the beet sugar market, particularly in India, China, and other developing nations. The food and beverages and dairy industries are expected to be the fastest-growing segments. \\n\\nKeywords: Beet sugar market, CAGR, natural sweeteners, beetroot juice extract, energy beverages, artisan beets, Asia Pacific, food and beverages industry, dairy industry.\\n', 'Summary: Batory Foods has established a new entity, Batory Sweetener Solutions, that will be dedicated to initiatives surrounding food and beverage sweeteners, including sugar reduction. Consumers are increasingly seeking reduced sugar and no-sugar-added options, and governments have implemented sugar taxes in response to the overconsumption of sugar and its links to metabolic diseases. The global sweeteners market is projected to reach $97.57 billion by 2030. Numerous ingredient suppliers have developed products to reduce sugar, including stevia, erythritol, chicory root fibers, prebiotic soluble fibers, and isomalt. Labels claiming reduced sugar and no-added-sugar must meet requirements laid out by regulatory bodies. \\r\\nKeywords: sugar reduction, sweeteners, Batory Foods, global market, consumer demand, sugar taxes, ingredient suppliers, stevia, erythritol, chicory root fibers, prebiotic soluble fibers, isomalt, regulation.\\n', \"Summary: The United Nations Secretary-General called for scientists to provide solid scientific guidance to push governments to curb climate change before crossing a key global warming threshold. The call comes following a meeting of experts and officials to finalize the last of seven reports issued by the global body's panel of top scientists since the Paris climate accord was forged in 2015.\\n\\nKeywords: United Nations, scientists, policies, climate change, global warming threshold, meeting, Paris climate accord, Intergovernmental Panel on Climate Change, greenhouse gas, fossil fuels.\\n\", \"Summary: GOOD GOOD® will showcase the US market's first sugar-free, vegan lemon curd at Natural Products ExpoWest in Anaheim featuring 77% fewer calories, 55% fewer carbs and 100% less sugar than current leaders on the market. They will also launch three new jam flavors. The company is known for its no sugar added jams, jellies, and spreads and aims to provide an experience that tastes good and is good for you while free from added sugar and artificial ingredients. \\n\\nKeywords: GOOD GOOD®, sugar-free, vegan, lemon curd, Natural Products ExpoWest, Anaheim, jams, jellies, spreads, no sugar added, innovation, keto, vegan lifestyles.\\n\", 'Summary: According to a report released by the Boao Forum for Asia, Asia will remain a crucial growth engine with an estimated 4.5% GDP expansion, making it a \"standout performer\" amidst the global economic slowdown. The report states that Asia\\'s weighted real GDP growth rate in 2023 is estimated to be 4.5%, an increase from 4.2% in 2022, with China and India contributing to half of the world\\'s growth this year. The report also calls for significant attention to the resilience of Asian economies, the reconfiguration of industrial chains, climate change responses, and the implementation of regional trade agreements.\\n\\nKeywords: Asia, GDP, growth, economy, China, India, Boao Forum for Asia, report, global economic slowdown, industrial chains, climate change, regional trade agreements.\\n', \"Summary: Bloomberg Surveillance covers the latest news in finance, economics, and investments. The news includes Goldman CEO's warning about bank rules affecting airfares and pensions, Boeing adding a new aircraft carrier to its fleet, Taiwan's economy outlook, Meituan's profit after Chinese travel growth, and more. \\n\\nKeywords: Bloomberg Surveillance, finance, economics, investments, bank rules, airfares, pensions, Boeing, aircraft carrier, Taiwan economy, Meituan profits, cryptocurrency, SenseTime, AI, Tesla, BlackRock, Australian houses.\\n\", \"Summary: The article discusses the violent history behind the sugar industry, including the transatlantic slave trade and the use of indentured labor. The article specifically focuses on the Canadian sugar industry's participation in these practices and the profits that were gained from them. The author argues for a better understanding of the origins of sugar and greater recognition for those who have been oppressed by the sugar industry. \\n\\nKeywords: sugar, history, transatlantic slave trade, indentured labor, Canadian sugar industry, profits, oppression.\\n\", 'Summary: A survey conducted by the World Action on Salt, Sugar & Health found that four out of five global producers selling food and drinks in Australia, France, and Mexico sell mostly unhealthy products. Kraft Heinz Co. ranked the worst, with 80% of its products failing health standards in all three markets. Kellogg Co. ranked next with 72% of its products not meeting health criteria. Nestle SA declined to comment. Danone ranked best with only 35% of its products scoring below healthy standards. Producers need to improve the nutritional content of their food and drink products to improve public health, according to Mhairi Brown, policy and public affairs lead with WASSH. This is also because obesity is a public health crisis in some countries and on the rise in the developing world. Investors like ShareAction are calling for companies to be more transparent about the healthiness of their portfolios to help investors evaluate the threat of potential anti-junk food legislation on sales. \\n\\nKeywords: survey, unhealthy food, health standards, Kraft Heinz, Kellogg, Nestle, Danone, public health, obesity, investors, transparency.\\n', 'Summary: The global reduced sugar food and beverage market is expected to reach $79.5 billion by 2028, with a market growth of 8.6% CAGR. The market demand for fruit snacks with decreased sugar is increasing due to the shift in customer preferences towards healthy convenience foods. The COVID-19 pandemic has impacted the market by causing an increase in sales of ready-to-eat foods, but rising health concerns related to sanitary and safety of processed foods have led to consumers opting for raw ingredients to prepare meals at home. The market growth factors include the rising prevalence of obesity and diseases caused by lifestyle. Concerns regarding the safety profile of artificial sweeteners are hindering market expansion.\\n\\nKeywords: Global, Reduced Sugar Food & Beverages Market, Market Growth, Fruit snacks, COVID-19 Impact, Obesity, Artificial sweeteners, Sanitary and safety of processed foods\\n', \"Summary: The news text is a collection of random headlines and short news stories covering various topics such as CIBC's quarterly earnings beating estimates, a documentary about a cryptocurrency exchange, Singapore's falling real income, etc. There is also news related to climate change, gun violence, and a surge in sugar prices leading buyers to delay international purchases.\\n\\nKeywords: CIBC, earnings, cryptocurrency exchange, Singapore, income, climate change, gun violence, sugar prices.\\n\", 'Summary: Sugar prices in New York have fallen by 1.4% after hitting a decade high due to concerns about tight global supplies caused by limited exports out of India and concerns about production in other key growers, leading to a world shortage. The May white-sugar contract is set to expire on Friday, and large open interest signals that some traders without physical supplies may need to close out short positions, supporting prices. The recent rally has pushed futures markets into overbought territory and may add to costs for manufacturers of everything from fizzy drinks to baked goods and maintain pressure on global food inflation.\\n\\nKeywords: Sugar prices, New York, tight global supplies, limited exports, India, world shortage, May white-sugar contract, overbought territory, global food inflation.\\n', 'Summary: Sugar prices in India have increased by more than 6% in two weeks due to falling production levels in Maharashtra, the top sugar producing state in the country. This is likely to strengthen demand from bulk consumers during the peak summer season and could lead to further price increases. While this will improve the margins of sugar makers, it could also cause elevated food inflation and discourage the Indian government from allowing additional sugar exports, which could support global prices. Keywords: India, sugar prices, production, Maharashtra, demand, summer season, inflation, sugar exports, global prices. \\n\\nNote: The last paragraph of the noisy text appears to be some general information about Reuters and its services, and is not relevant to the main news story. The other two paragraphs, however, contain information about sugar prices and related industries in India.\\n', 'Summary: N/A\\nKeywords: KoreaTimes, Copyright, All rights reserved\\n', \"Summary: The article contains several news items related to Korea, including franchise fraud and SK group's decision to not invest further in troubled online retailer 11Street, rising tariffs on pork, mackerel, and sugar, as well as the popularity of Tanghulu (a traditional Chinese snack) in Korea despite health risks. There is also mention of a zero-sugar soju that is gaining popularity among health-conscious consumers.\\n\\n\\nKeywords: Korea, franchise fraud, SK group, online retailer, tariffs, pork, mackerel, sugar, tanghulu, snack, zero-sugar, soju.\\n\", 'Summary: The study evaluated the quality of evidence, potential biases, and validity of available studies examining the impact of dietary sugar consumption on health outcomes. The umbrella review of 73 meta-analyses found significant harmful associations between dietary sugar consumption and multiple health outcomes, including endocrine/metabolic, cardiovascular, cancer, and other outcomes such as neuropsychiatric, dental, hepatic, osteal, and allergic. The review also recommended reducing free/added sugar consumption to below 25 g/day and limiting sugar-sweetened beverage consumption to less than one serving/week to reduce the adverse effects on health.\\n\\nKeywords: dietary sugar consumption, health outcomes, meta-analyses, harmful associations, free sugars, added sugars, sugar-sweetened beverages, reducing consumption\\n', \"Summary: Top shareholders at Byju’s are demanding certain conditions before any future capital infusion into the edtech firm battling a deepening fund crunch. Companies are paying a premium to advertise through 3D-animated humans or virtual influencers on Instagram. Hamid Ahmed describes the timing of the Burman family open offer to buy more shares in Religare Enterprises as 'fishy'. Gold prices will be impacted by Fed moves, geopolitical scenarios, and upcoming polls. India is struggling with the spread of COPD to rural areas. \\n\\nKeywords: Byju's, edtech, capital infusion, shareholders, fund crunch, virtual influencers, Instagram, advertising, Religare Enterprises, Burman family, shares, gold prices, Fed moves, geopolitical scenarios, COPD, India.\\n\", \"Summary: Indian sugar mills produced 31.1 million tonnes of sugar, representing a fall of 5.4% year on year due to many mills closing early because of limited sugar cane availability which will leave hardly any surplus for additional exports during the 2022/23 season. Maharashtra had the biggest drop with production falling from 13.7 million to 10.5 million tonnes last year. India exported a record 11.2 million tonnes of sugar in the previous 2021/22 season and could boost global prices should India not export any sugar this season. Keywords: India, sugar production, sugar mills, sugar exports, Maharashtra. \\n\\nNote: The news webpage also includes information about Taiwan's health ministry urging some people to avoid travel to China due to respiratory illnesses, as well as information about services provided by Reuters. However, these pieces of information are not related to the relevant news topic of India's sugar production and exportation.\\n\", 'Summary: Eating too many refined wheat and rice products, along with eating too few whole grains, is fueling the growth of new cases of type 2 diabetes worldwide, according to a new study that models data through 2018. Additionally, people are eating far too much red and processed meats such as bacon, sausage, salami and the like. Those three factors were the primary drivers of over 14 million new cases of type 2 diabetes in 2018. Researchers found that over 60% of diet-attributable cases of the disease were due to excess intake of just six harmful dietary habits: eating too much refined rice, wheat and potatoes; too many processed and unprocessed red meats; and drinking too many sugar-sweetened beverages and fruit juice. Low intake of fruits, nonstarchy vegetables, nuts, seeds, whole grains and yogurt was responsible for just over 39% of the new cases. People in Eastern and Central Europe as well as Central Asia had the highest percentage of new type 2 diabetes cases linked to diet, while Colombia, Mexico and other countries in Latin America and the Caribbean also had high numbers of new cases. \\n\\nKeywords: refined grains, whole grains, red meat, processed meat, type 2 diabetes, diet, sugar-sweetened beverages, fruits, vegetables, nuts, seeds, yogurt, epidemiology.\\n', \"Summary: The United Nations’ food agency's world price index fell for the 12th consecutive month, dropping to its lowest level since last July due to ample supplies and subdued import demand. The decline in the index reflected lower prices for cereals, vegetable oils, and dairy products, which offset rises in sugar and meat prices. The FAO raised its forecast for world wheat production in 2023, which is now pegged at 786 million tonnes and cereal stocks are expected to ease by 0.3% from their opening levels to 850 million tonnes. On the other hand, OPEC member Nigeria is unlikely to reach its production target in 2024 after years of declining output, according to figures from consultancies.\\nKeywords: FAO, food price index, cereals, vegetable oils, sugar, meat, world wheat production, Nigeria, OPEC.\\n\", 'Summary: This is a collection of headlines and snippets of news articles from various sources covering topics such as business and finance, cryptocurrency, climate change, and sports. Some of the headlines include CIBC earnings beating estimates, the euro-area inflation slowing more than expected, and a documentary about the collapse of a cryptocurrency exchange. \\n\\nKeywords: business, finance, cryptocurrency, CIBC earnings, euro-area inflation, documentary, collapse, sugar, climate change, sports.\\n', \"Summary: The news data is too noisy and doesn't have any relevant information.\\n\\nKeywords: N/A\\n\", 'Summary: Brazil is expected to produce 40.3 million tonnes of sugar in the new season, and mills will allocate a near record amount of sugarcane to sugar production at 46.7%. Sugar production is seen growing by 3.15 million tonnes from the previous crop, while ethanol production is seen growing by 1.8 billion liters to a total of 33.5 billion liters. Brazilian exports are expected to grow by 2.67 million tonnes in 2023/24 to 29.75 million tonnes. The good production level in Brazil will prevent a large deficit in the global supply of sugar. \\n\\nKeywords: Brazil, sugar, production, mills, sugarcane, ethanol, exports, global supply.\\n', 'Summary: The global sugar syrup market was valued at USD 2.3 billion in 2022 and is expected to reach USD 3.2 billion by 2030, with a CAGR of 5.2% over the forecast period 2023-2030. The growth of the market is due to the increasing demand for processed foods and beverages, the growing popularity of natural sweeteners, and the rising demand for convenience foods. The corn syrup segment is expected to generate the majority of the revenue due to its increasing demand. The North American region is anticipated to produce about half of the global revenue of the sugar syrup market, while the Asia Pacific region is expected to witness the fastest growth. \\n\\nKeywords: sugar syrup market, CAGR, processed foods, natural sweeteners, convenience foods, corn syrup, North America, Asia Pacific.\\n', 'Summary: Eli Lilly is selling its nasal powder rescue treatment for severe hypoglycemia, Baqsimi, to Amphastar for $500 million in cash upfront, with an additional $125 million in cash upon the one-year anniversary of the deal’s close. Lilly will also receive sales-based milestones worth up to $450 million. The sale is expected to close in Q3 2023. Baqsimi hit the market in 2019 and generated $139.3 million in sales last year. Lilly recently slashed the prices of its insulins and is focusing on its newest Type 2 diabetes offering, Mounjaro. Amphastar has a global presence, developing and selling injectables, intranasal drugs, and inhalation products, including a glucagon product. \\n\\nKeywords: Eli Lilly, nasal powder rescue treatment, severe hypoglycemia, diabetes, Baqsimi, Amphastar, sale, insulins, Mounjaro, glucagon, insulin price-capping, Novo Nordisk, Sanofi, GIP/GLP-1, obesity, phase 3b trial.\\n', 'Summary: A new report from Feedback and Action on Sugar highlights the role of supermarkets in perpetuating dangerous levels of sugar consumption in the UK. Nine out of ten supermarkets lack policies to measure total sugar sales and set reduction targets. Overall sugar consumption remains at twice the healthy level in the UK, and voluntary measures such as the Sugar Reduction Programme have been ineffective, with a 7% increase in supermarket sugar sales reported last year. The report calls for urgent legislation to track and reduce total supermarket sugar sales.\\n\\nKeywords: Sugar consumption, UK, Feedback and Action on Sugar, supermarkets, public health challenges, obesity, childhood tooth decay, type 2 diabetes, legislation, Sugar Reduction Programme, voluntary measures.\\n']\n",
            "\n",
            "    Now analyze the commodity's price movement from 03/19/2023 to 04/24/2023. Only use the prices provided.\n",
            "    Provide a Summary and an analysis of the Commodity Price Movement.\n",
            "    The analysis should comprehensively explain the reasons, key factors and events that influenced the price movement.\n",
            "    Do not just summarize the history. Reason step by step before the finalized output.\n",
            "    Use format Summary: ..., Commodity Price Movement Analysis: ...\n",
            "    Use bulletpoints for structuring the different factors and events in the analysis.\n",
            "    \n"
          ]
        },
        {
          "output_type": "error",
          "ename": "RateLimitError",
          "evalue": "ignored",
          "traceback": [
            "\u001b[0;31m---------------------------------------------------------------------------\u001b[0m",
            "\u001b[0;31mRateLimitError\u001b[0m                            Traceback (most recent call last)",
            "\u001b[0;32m<ipython-input-19-0ec70ae8bb64>\u001b[0m in \u001b[0;36m<cell line: 1>\u001b[0;34m()\u001b[0m\n\u001b[0;32m----> 1\u001b[0;31m \u001b[0mprint\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mgenerate_commodity_response\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34m'03/19/2023'\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0;34m'04/24/2023'\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0;34m'globalsugar'\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0;34m'analysis'\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m",
            "\u001b[0;32m<ipython-input-18-616393e79744>\u001b[0m in \u001b[0;36mgenerate_commodity_response\u001b[0;34m(start_date, end_date, commodity, prompt)\u001b[0m\n\u001b[1;32m     14\u001b[0m     \u001b[0mprint\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mgenerated_prompt\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m     15\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m---> 16\u001b[0;31m     response = client.chat.completions.create(\n\u001b[0m\u001b[1;32m     17\u001b[0m         \u001b[0mmodel\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0;34m\"GPT35\"\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m     18\u001b[0m         messages=[\n",
            "\u001b[0;32m/usr/local/lib/python3.10/dist-packages/openai/_utils/_utils.py\u001b[0m in \u001b[0;36mwrapper\u001b[0;34m(*args, **kwargs)\u001b[0m\n\u001b[1;32m    299\u001b[0m                         \u001b[0mmsg\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0;34mf\"Missing required argument: {quote(missing[0])}\"\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    300\u001b[0m                 \u001b[0;32mraise\u001b[0m \u001b[0mTypeError\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mmsg\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m--> 301\u001b[0;31m             \u001b[0;32mreturn\u001b[0m \u001b[0mfunc\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34m*\u001b[0m\u001b[0margs\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0;34m**\u001b[0m\u001b[0mkwargs\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m    302\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    303\u001b[0m         \u001b[0;32mreturn\u001b[0m \u001b[0mwrapper\u001b[0m  \u001b[0;31m# type: ignore\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;32m/usr/local/lib/python3.10/dist-packages/openai/resources/chat/completions.py\u001b[0m in \u001b[0;36mcreate\u001b[0;34m(self, messages, model, frequency_penalty, function_call, functions, logit_bias, max_tokens, n, presence_penalty, response_format, seed, stop, stream, temperature, tool_choice, tools, top_p, user, extra_headers, extra_query, extra_body, timeout)\u001b[0m\n\u001b[1;32m    596\u001b[0m         \u001b[0mtimeout\u001b[0m\u001b[0;34m:\u001b[0m \u001b[0mfloat\u001b[0m \u001b[0;34m|\u001b[0m \u001b[0mhttpx\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mTimeout\u001b[0m \u001b[0;34m|\u001b[0m \u001b[0;32mNone\u001b[0m \u001b[0;34m|\u001b[0m \u001b[0mNotGiven\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0mNOT_GIVEN\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    597\u001b[0m     ) -> ChatCompletion | Stream[ChatCompletionChunk]:\n\u001b[0;32m--> 598\u001b[0;31m         return self._post(\n\u001b[0m\u001b[1;32m    599\u001b[0m             \u001b[0;34m\"/chat/completions\"\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    600\u001b[0m             body=maybe_transform(\n",
            "\u001b[0;32m/usr/local/lib/python3.10/dist-packages/openai/_base_client.py\u001b[0m in \u001b[0;36mpost\u001b[0;34m(self, path, cast_to, body, options, files, stream, stream_cls)\u001b[0m\n\u001b[1;32m   1094\u001b[0m             \u001b[0mmethod\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0;34m\"post\"\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0murl\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0mpath\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mjson_data\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0mbody\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mfiles\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0mto_httpx_files\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mfiles\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0;34m**\u001b[0m\u001b[0moptions\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m   1095\u001b[0m         )\n\u001b[0;32m-> 1096\u001b[0;31m         \u001b[0;32mreturn\u001b[0m \u001b[0mcast\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mResponseT\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mself\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mrequest\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mcast_to\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mopts\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mstream\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0mstream\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mstream_cls\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0mstream_cls\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m   1097\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m   1098\u001b[0m     def patch(\n",
            "\u001b[0;32m/usr/local/lib/python3.10/dist-packages/openai/_base_client.py\u001b[0m in \u001b[0;36mrequest\u001b[0;34m(self, cast_to, options, remaining_retries, stream, stream_cls)\u001b[0m\n\u001b[1;32m    854\u001b[0m         \u001b[0mstream_cls\u001b[0m\u001b[0;34m:\u001b[0m \u001b[0mtype\u001b[0m\u001b[0;34m[\u001b[0m\u001b[0m_StreamT\u001b[0m\u001b[0;34m]\u001b[0m \u001b[0;34m|\u001b[0m \u001b[0;32mNone\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0;32mNone\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    855\u001b[0m     ) -> ResponseT | _StreamT:\n\u001b[0;32m--> 856\u001b[0;31m         return self._request(\n\u001b[0m\u001b[1;32m    857\u001b[0m             \u001b[0mcast_to\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0mcast_to\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    858\u001b[0m             \u001b[0moptions\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0moptions\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;32m/usr/local/lib/python3.10/dist-packages/openai/_base_client.py\u001b[0m in \u001b[0;36m_request\u001b[0;34m(self, cast_to, options, remaining_retries, stream, stream_cls)\u001b[0m\n\u001b[1;32m    892\u001b[0m             \u001b[0;32mif\u001b[0m \u001b[0mretries\u001b[0m \u001b[0;34m>\u001b[0m \u001b[0;36m0\u001b[0m \u001b[0;32mand\u001b[0m \u001b[0mself\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0m_should_retry\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0merr\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mresponse\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    893\u001b[0m                 \u001b[0merr\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mresponse\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mclose\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m--> 894\u001b[0;31m                 return self._retry_request(\n\u001b[0m\u001b[1;32m    895\u001b[0m                     \u001b[0moptions\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    896\u001b[0m                     \u001b[0mcast_to\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;32m/usr/local/lib/python3.10/dist-packages/openai/_base_client.py\u001b[0m in \u001b[0;36m_retry_request\u001b[0;34m(self, options, cast_to, remaining_retries, response_headers, stream, stream_cls)\u001b[0m\n\u001b[1;32m    964\u001b[0m         \u001b[0mtime\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0msleep\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mtimeout\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    965\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m--> 966\u001b[0;31m         return self._request(\n\u001b[0m\u001b[1;32m    967\u001b[0m             \u001b[0moptions\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0moptions\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    968\u001b[0m             \u001b[0mcast_to\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0mcast_to\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;32m/usr/local/lib/python3.10/dist-packages/openai/_base_client.py\u001b[0m in \u001b[0;36m_request\u001b[0;34m(self, cast_to, options, remaining_retries, stream, stream_cls)\u001b[0m\n\u001b[1;32m    892\u001b[0m             \u001b[0;32mif\u001b[0m \u001b[0mretries\u001b[0m \u001b[0;34m>\u001b[0m \u001b[0;36m0\u001b[0m \u001b[0;32mand\u001b[0m \u001b[0mself\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0m_should_retry\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0merr\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mresponse\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    893\u001b[0m                 \u001b[0merr\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mresponse\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mclose\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m--> 894\u001b[0;31m                 return self._retry_request(\n\u001b[0m\u001b[1;32m    895\u001b[0m                     \u001b[0moptions\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    896\u001b[0m                     \u001b[0mcast_to\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;32m/usr/local/lib/python3.10/dist-packages/openai/_base_client.py\u001b[0m in \u001b[0;36m_retry_request\u001b[0;34m(self, options, cast_to, remaining_retries, response_headers, stream, stream_cls)\u001b[0m\n\u001b[1;32m    964\u001b[0m         \u001b[0mtime\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0msleep\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mtimeout\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    965\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m--> 966\u001b[0;31m         return self._request(\n\u001b[0m\u001b[1;32m    967\u001b[0m             \u001b[0moptions\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0moptions\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    968\u001b[0m             \u001b[0mcast_to\u001b[0m\u001b[0;34m=\u001b[0m\u001b[0mcast_to\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;32m/usr/local/lib/python3.10/dist-packages/openai/_base_client.py\u001b[0m in \u001b[0;36m_request\u001b[0;34m(self, cast_to, options, remaining_retries, stream, stream_cls)\u001b[0m\n\u001b[1;32m    906\u001b[0m                 \u001b[0merr\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mresponse\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mread\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    907\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m--> 908\u001b[0;31m             \u001b[0;32mraise\u001b[0m \u001b[0mself\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0m_make_status_error_from_response\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0merr\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mresponse\u001b[0m\u001b[0;34m)\u001b[0m \u001b[0;32mfrom\u001b[0m \u001b[0;32mNone\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m    909\u001b[0m         \u001b[0;32mexcept\u001b[0m \u001b[0mhttpx\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mTimeoutException\u001b[0m \u001b[0;32mas\u001b[0m \u001b[0merr\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    910\u001b[0m             \u001b[0;32mif\u001b[0m \u001b[0mresponse\u001b[0m \u001b[0;32mis\u001b[0m \u001b[0;32mnot\u001b[0m \u001b[0;32mNone\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;31mRateLimitError\u001b[0m: Error code: 429 - {'error': {'code': '429', 'message': 'Requests to the Creates a completion for the chat message Operation under Azure OpenAI API version 2023-05-15 have exceeded call rate limit of your current OpenAI S0 pricing tier. Please go here: https://aka.ms/oai/quotaincrease if you would like to further increase the default rate limit.'}}"
          ]
        }
      ]
    }
  ]
}