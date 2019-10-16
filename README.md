# analyticsFinance
Dash Plotly Interactive MultiPage Web Dashboard analysing the financial information of over 5000 publicly trading companies between 2009 and 2018 - WIP

*Author Jelena Lor*

*October 2019*

**Current version running on**
https://dash-finapp.herokuapp.com/

**WebApp** <br>
With this WebApp a user can analyse the financial performance of various company's and industries.
An interactive features means the patterns can be explored across time and compared between companies.

**Use Cases**
1. Find the industry with the least amount of companies and the most stable and highest share price. See the share price distribution by industry. Compare the number of companies versus average share price per industry. 
2. Find the best performing company (based on your chosen metrics) within the chosen industry. See the chosen company's financial performance over the last 10 years.
4. Compare the performance of up to 3 companies across major metrics, such as Revenue, Profit, Assets, EPS, Debt to Equity ratio. Identify momenteraly if the company's performance comes at the cost of high debt etc. 
5. Find the companies for comparison based on: industry, company's symbol, max or min of specific metrics etc.


**Data** <br>
Dataset is publicly available and shows the income statement, balance sheet and various financial metric values for over 5,000 publicly traded companies between 2009 and 2018. 
For example, company's revenue, profit, total assets, EPS etc

Sourced from https://financialmodelingprep.com

**Dependencies:**
* Dash
* Plotly


**Images of the dashboard**

![Capture](https://user-images.githubusercontent.com/31029142/66709682-4d74df80-ed37-11e9-8d72-e7a7648f0a50.PNG)


![Capture2](https://user-images.githubusercontent.com/31029142/66709677-4cdc4900-ed37-11e9-9dc9-a4e6a92c5c4b.PNG)


![Capture3](https://user-images.githubusercontent.com/31029142/66709678-4cdc4900-ed37-11e9-9f83-228071bb5c80.PNG)


![Capture4](https://user-images.githubusercontent.com/31029142/66709679-4d74df80-ed37-11e9-917a-47d78144a740.PNG)


![Capture5](https://user-images.githubusercontent.com/31029142/66709680-4d74df80-ed37-11e9-8eee-c594f37a298f.PNG)


![Capture6](https://user-images.githubusercontent.com/31029142/66709681-4d74df80-ed37-11e9-9ff0-7881bbd9e475.PNG)



**Future improvements**

The data is found to be sometimes incorrect showing inflated figures. Need to come up with an algorithm to clean up the values and get rid of outliers. Tried a simple > 3 std but did not seem to yield a good result. 

WIP
