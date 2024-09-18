## Data Description:
The dataset consists of the following columns:

- index: An unique identifier (ID) for the data sample
- image_link: Public URL where the product image is available for download. Example link - https://m.media-amazon.com/images/I/71XfHPR36-L.jpg
- To download images use download_images function from src/utils.py. See sample code in src/test.ipynb.
- group_id: Category code of the product
- entity_name: Product entity name. For eg: “item_weight”
- entity_value: Product entity value. For eg: “34 gram”
Note: For test.csv, you will not see the column entity_value as it is the target variable.
