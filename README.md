# AQMD

![Image description](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/pw93cnyur18dmo46ivnk.png)

Air Quality Monitoring Delivery - Project created for an event under the Social impact / Sustainability category. Idea is to make use of Battery operated Government Garbage collector vehicle to track air pollution in each street.

# Problem Statement 

We know that the intensity of air pollution is increasing all over the places, yet we are ignoring this fact in an assumption that we are immune to it. It is found recently by scientists that how bad this could impact us. Health impacts extends way beyond the respiratory illness. Through research it is found that , foetal development ,mental health and metabolic syndrome are impacted due to increase in air pollution. 

Based on Dr. Sarath Guttikunda article, “A general understanding is that an ambient monitoring station can represent an area covering 2 km radius, which translates to 15 sq.km (rounded off).” But if we consider Chennai Metropolitan area, it is spread across 1189 sq km (planned to expand up to 8878 sq km), whereas we have only 8 air quality monitoring stations as of 23rd Jan 2023. It is evident that we don’t have enough stations to cover entire area. 

Proposed solution is to make use of BOV Garbage Collector, food delivery partners/ Cabs (Ola, Uber, Swiggy, Zomato …etc.) to mount the air quality sensor that detects PM 2.5, 10 concentrations in the air and visualize it as a live heat map. It will be an effective solution than ambient monitoring station as it shows us exactly where the intensity of air pollution is higher on street basis.

![](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/tj5actpkp3vo06j07vy4.png)

# Architecutre

![Image description](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/4ubgoferawvx7pqrgpp9.png)

# DataFlow

- IoT devices push the telemetry to cloud gateway (IoT Hub)
- Message routing feature of IoT hub enables us to forward the telemetry to different store path. In our proposed   architecture we have used Azure Cosmos DB as a hot store path to store data. Azure cosmos DB is ideal for IoT workloads as it is highly capable of ingesting high volume of data at low latency and high rates. IoT hub is also capable of filtering only specific messages to be pushed into Azure Cosmos DB.
- Hybrid Transactional and Analytical Processing (HTAP) capability of Azure Synapse link for Azure Cosmos DB integrates data into analytical store which is highly efficient for analytical purposes.
- Power BI helps us to visualize data in a Azure Map layer. Heat Map is used in our proposed architecture to better depict our scenario.
- Azure Cosmos DB change feed triggers an Azure Functions
- Change Feed trigger is used to publish the message to a Azure Web PubSub service 
- As a presentation layer we have a Azure Map integration in a web app and with the websockets we will have near real-time updates about the telemetry and could visualize it.

# Device Setup

![Image description](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/q9d2mw0ob553wgjxuhic.png)

# Ride with AQMD

![Image description](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/o28dxn602tq652w9agsz.png)


# Heatmap

![Image description](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/b4r0h21ahyroq49n7lcs.png)


# Sponsor

Leave a ⭐ if you like this project

<a href="https://www.buymeacoffee.com/divakarkumar" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 40px !important;width: 145 !important;" ></a>


&copy; [Divakar Kumar](//github.com/Divakar-Kumar)

For detailed documentation in PDF format , please visit the [docs](docs/AQMD.pdf). 

# Contact

[Website](//iamdivakarkumar.com) | [LinkedIn](https://www.linkedin.com/in/divakar-kumar/) | [AQMD](https://github.com/Cloud-Jas/AQMD)
