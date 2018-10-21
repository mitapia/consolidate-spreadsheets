# consolidate-spreadsheets
# Summary
Python program meant to take data from several spreadsheets and combine into one, merging any redundancies.

# Problem
The client, M&J Shoes, is doing an audit of their On-Hand inventory across multiple stores.  They have made spreadsheets of each of their stores. Each row represents a particular style and color with the following columns populated by the size found of said style-color. It is essentially a numerical image of what they found on their shelves.

## Samples:
### Store1
| Style        |     |     |     |
| ------------ |:---:|:---:|:---:|
| item-001     |  9  |  8  |  9  |

### Store2
| Style        |     |     |     |
| ------------ |:---:|:---:|:---:|
| item-001     |  9  |  9  |  9  |
| item-002     |  7  |  7  |  7  |



They require a single spreadsheet of the actual count of each unique item.  Each style, color, and size combination is its own item and must be counted individually per store.
The final spreadsheet should look like this:

| Style        | Size | Store1 QTY | Store2 QTY |
| ------------ |:----:|:----------:|:----------:|
| item-001     | 8    |     1      |      0     |
| item-001     | 9    |     2      |      3     |
| item-002     | 7    |     0      |      3     |


# Solution
This python program will take all the spreadsheets the client already has and compiled them into the desired format of the final spreadsheet.  For each style-color row, we will count the sizes that appear in the proceeding columns.  When reading a new dataset from another store it will first check if the item has already been created in the final spreadsheet, if so it will simply go to its corresponding Qty column and update the appropriate count instead of making a duplicate item row.
