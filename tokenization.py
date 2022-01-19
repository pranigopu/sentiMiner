{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Dataset"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Full dataset"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 169,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "COLUMN NAMES\n",
      "------------\n",
      "id\n",
      "dateAdded\n",
      "dateUpdated\n",
      "name\n",
      "brand\n",
      "categories\n",
      "primaryCategories\n",
      "manufacturer\n",
      "manufacturerNumber\n",
      "reviews.date\n",
      "reviews.doRecommend\n",
      "reviews.numHelpful\n",
      "reviews.rating\n",
      "reviews.text\n",
      "reviews.title\n"
     ]
    }
   ],
   "source": [
    "import pandas as pd\n",
    "# The whole data set\n",
    "data = pd.read_csv(\"data/amazonConsumerReviews.csv\")\n",
    "print(\"COLUMN NAMES\\n------------\")\n",
    "for c in data.columns: print(c)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Only keeping relevant columns"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 92,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>id</th>\n",
       "      <th>reviews.doRecommend</th>\n",
       "      <th>reviews.rating</th>\n",
       "      <th>reviews.text</th>\n",
       "      <th>reviews.title</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>AVqVGZNvQMlgsOJE6eUY</td>\n",
       "      <td>False</td>\n",
       "      <td>3</td>\n",
       "      <td>I thought it would be as big as small paper bu...</td>\n",
       "      <td>Too small</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>AVqVGZNvQMlgsOJE6eUY</td>\n",
       "      <td>True</td>\n",
       "      <td>5</td>\n",
       "      <td>This kindle is light and easy to use especiall...</td>\n",
       "      <td>Great light reader. Easy to use at the beach</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>AVqVGZNvQMlgsOJE6eUY</td>\n",
       "      <td>True</td>\n",
       "      <td>4</td>\n",
       "      <td>Didnt know how much i'd use a kindle so went f...</td>\n",
       "      <td>Great for the price</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "                     id  reviews.doRecommend  reviews.rating  \\\n",
       "0  AVqVGZNvQMlgsOJE6eUY                False               3   \n",
       "1  AVqVGZNvQMlgsOJE6eUY                 True               5   \n",
       "2  AVqVGZNvQMlgsOJE6eUY                 True               4   \n",
       "\n",
       "                                        reviews.text  \\\n",
       "0  I thought it would be as big as small paper bu...   \n",
       "1  This kindle is light and easy to use especiall...   \n",
       "2  Didnt know how much i'd use a kindle so went f...   \n",
       "\n",
       "                                  reviews.title  \n",
       "0                                     Too small  \n",
       "1  Great light reader. Easy to use at the beach  \n",
       "2                           Great for the price  "
      ]
     },
     "execution_count": 92,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# Only selecting relevant columns\n",
    "reviewsData = data[['id',\n",
    "                  'reviews.doRecommend',\n",
    "                  'reviews.rating',\n",
    "                  'reviews.text',\n",
    "                  'reviews.title']]\n",
    "reviewsData.head(3)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Converting ratings into sentiment labels"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 93,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "REVIEWS RATING INFO\n",
      "------------\n",
      "Minimum: 1\n",
      "Maximum: 5\n",
      "Mean: 4.5968\n"
     ]
    }
   ],
   "source": [
    "print(\"REVIEWS RATING INFO\\n------------\")\n",
    "ratings = reviewsData['reviews.rating']\n",
    "print(\"Minimum:\", min(ratings))\n",
    "print(\"Maximum:\", max(ratings))\n",
    "print(\"Mean:\", sum(ratings)/len(ratings))"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "For our purposes, let rating < 3 mean negative, rating > 3 mean positive, and rating = 3 be neutral."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 94,
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "<ipython-input-94-b5cb7473bffd>:7: SettingWithCopyWarning: \n",
      "A value is trying to be set on a copy of a slice from a DataFrame.\n",
      "Try using .loc[row_indexer,col_indexer] = value instead\n",
      "\n",
      "See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy\n",
      "  reviewsData['sentiment'] = sentiment\n"
     ]
    },
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>id</th>\n",
       "      <th>reviews.doRecommend</th>\n",
       "      <th>reviews.text</th>\n",
       "      <th>reviews.title</th>\n",
       "      <th>sentiment</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>AVqVGZNvQMlgsOJE6eUY</td>\n",
       "      <td>False</td>\n",
       "      <td>I thought it would be as big as small paper bu...</td>\n",
       "      <td>Too small</td>\n",
       "      <td>n</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>AVqVGZNvQMlgsOJE6eUY</td>\n",
       "      <td>True</td>\n",
       "      <td>This kindle is light and easy to use especiall...</td>\n",
       "      <td>Great light reader. Easy to use at the beach</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>AVqVGZNvQMlgsOJE6eUY</td>\n",
       "      <td>True</td>\n",
       "      <td>Didnt know how much i'd use a kindle so went f...</td>\n",
       "      <td>Great for the price</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "                     id  reviews.doRecommend  \\\n",
       "0  AVqVGZNvQMlgsOJE6eUY                False   \n",
       "1  AVqVGZNvQMlgsOJE6eUY                 True   \n",
       "2  AVqVGZNvQMlgsOJE6eUY                 True   \n",
       "\n",
       "                                        reviews.text  \\\n",
       "0  I thought it would be as big as small paper bu...   \n",
       "1  This kindle is light and easy to use especiall...   \n",
       "2  Didnt know how much i'd use a kindle so went f...   \n",
       "\n",
       "                                  reviews.title sentiment  \n",
       "0                                     Too small         n  \n",
       "1  Great light reader. Easy to use at the beach         1  \n",
       "2                           Great for the price         1  "
      ]
     },
     "execution_count": 94,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# Converting ratings to sentiment labels\n",
    "sentiment = []\n",
    "for r in ratings:\n",
    "    if r < 3: sentiment.append(0)   # Negative\n",
    "    elif r > 3: sentiment.append(1) # Positive\n",
    "    else: sentiment.append('n')     # Neutral\n",
    "reviewsData['sentiment'] = sentiment\n",
    "try: del(reviewsData['reviews.rating'])\n",
    "except: pass\n",
    "reviewsData.head(3)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Removing neutral sentiment rows"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 97,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>id</th>\n",
       "      <th>reviews.doRecommend</th>\n",
       "      <th>reviews.text</th>\n",
       "      <th>reviews.title</th>\n",
       "      <th>sentiment</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>AVqVGZNvQMlgsOJE6eUY</td>\n",
       "      <td>True</td>\n",
       "      <td>This kindle is light and easy to use especiall...</td>\n",
       "      <td>Great light reader. Easy to use at the beach</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>AVqVGZNvQMlgsOJE6eUY</td>\n",
       "      <td>True</td>\n",
       "      <td>Didnt know how much i'd use a kindle so went f...</td>\n",
       "      <td>Great for the price</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>AVqVGZNvQMlgsOJE6eUY</td>\n",
       "      <td>True</td>\n",
       "      <td>I am 100 happy with my purchase. I caught it o...</td>\n",
       "      <td>A Great Buy</td>\n",
       "      <td>1</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "                     id  reviews.doRecommend  \\\n",
       "1  AVqVGZNvQMlgsOJE6eUY                 True   \n",
       "2  AVqVGZNvQMlgsOJE6eUY                 True   \n",
       "3  AVqVGZNvQMlgsOJE6eUY                 True   \n",
       "\n",
       "                                        reviews.text  \\\n",
       "1  This kindle is light and easy to use especiall...   \n",
       "2  Didnt know how much i'd use a kindle so went f...   \n",
       "3  I am 100 happy with my purchase. I caught it o...   \n",
       "\n",
       "                                  reviews.title sentiment  \n",
       "1  Great light reader. Easy to use at the beach         1  \n",
       "2                           Great for the price         1  \n",
       "3                                   A Great Buy         1  "
      ]
     },
     "execution_count": 97,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# Removing neutral rows\n",
    "reviewsData = reviewsData[reviewsData['sentiment'] != 'n']\n",
    "# Hence we can see the first row (which has neutral sentiment label) will be removed\n",
    "reviewsData.head(3)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Tokenization"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 100,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Tokenising the words within the reviews\n",
    "from tensorflow.keras.preprocessing.text import Tokenizer\n",
    "reviews = reviewsData['reviews.text'].values\n",
    "tokenizer = Tokenizer(num_words = 5000)\n",
    "tokenizer.fit_on_texts(reviews)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "The 'Tokenizer' class enables you to tokenize text. Tokenizing text is the process of breaking a text into tokens (usually individual words)."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 183,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "ENCODED:\n",
      "[1, 42, 2, 21, 12, 13, 43, 13, 22, 44, 14, 45, 23, 6, 12, 46, 47, 5, 48, 1, 49, 2, 9, 50, 22, 6, 24, 25, 2, 51, 52, 53, 13, 54, 7, 21, 55, 56, 3, 26, 57] \n",
      "\n",
      "ORIGINAL:\n",
      "I thought it would be as big as small paper but turn out to be just like my palm. I think it is too small to read on it... not very comfortable as regular Kindle. Would definitely recommend a paperwhite instead.\n"
     ]
    }
   ],
   "source": [
    "# Replacing words with their respective indices\n",
    "# (The indices can be seen using the 'word_index' attribute of the 'Tokenizer' object)\n",
    "encodedDocs = tokenizer.texts_to_sequences(reviews)\n",
    "\n",
    "# Comparing element of 'encodedDocs' to corresponding element of 'reviews'\n",
    "print(\"ENCODED:\")\n",
    "print(encodedDocs[0], \"\\n\")\n",
    "print(\"ORIGINAL:\")\n",
    "print(reviews[0])"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
