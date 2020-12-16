# Enforce-BGP: Use Reinforcement Learning to detect Border Gateway Protocol (BGP) IP Prefix Hijacking

![Cover](https://github.com/niyuzheno1/Enforce-BGP/blob/main/cover.png?raw=true)

![Table](https://github.com/niyuzheno1/Enforce-BGP/blob/main/table.JPG?raw=true)




## Inspiration

We want to find energy efficient and high accurate solution for solving BGP Hijacking detection. Traditional approaches like tabulations will incur significant overhead and it is not efficient in terms of identifying BGP anomalies due to the nature of the attack being trasient and non-volumetric. In this repository, we will develop an effective methods in identifying BGP anomalies in almost real time. 

## What it does

Problem
Given a history of BGP update information from Routeview, I want to find a way that can minimize the amount of false positive rates in identifying BGP IP Hijacking anomaly.
Input
Historical data of BGP updates from Jan 2016-Oct 2020 from Routeview. 
Output
The set of BGP updates that are evidence of IP Hijacking
Secondary Input
A specific IP address
Secondary Output
A set of ASes that have announced this IP address or an CIDR that encompassed this IP address.

## How I built it

Frontend:  React.js, d3.js, dc.js

Backend: Tensorflow, MRTParser, GeoIP, 

Deployment: Pythonanywhere, CodeSandbox

![Tools](https://github.com/niyuzheno1/Enforce-BGP/blob/main/tools.JPG?raw=true)


## Challenges I ran into

During our implementation, we have faced a lot of challenges These challenges typically include a better incorporation of frontend and backend, a better incorporation of different libraries and  incorporation of existing knowledge to our visualization. For one of these challenges, we face when we update an AS, we will have two copies of graph overlapping together. The reason is that we used D3 and React together and they are not compatible well together. The second challenge we face is to use appropriate algorithms in visualizing the BGP graph. We first chose to use DFS for the BGP plot. But it was not approachable because when we truncated the number of vertices, it will always cause us to have a cluster. It does not well represent the neighborhood of a vertex (autonomous system). We decided to use BFS, instead. 


## Accomplishments that I'm proud of

I am able to stick with what I proposed during the begining of the quarter. I was able to faithfully follow what I want to prove. 

## What I learned

I have learned that there are a lot of challenges in developing good approach in identifying BGP hijacking anomaly. It was hard or even impossible for me to know what exactly was going on behind the scene at the first place. But I was somehow managed to find an approach in understanding BGP update message and I was able to find the best way to finalize a set of features for my DQN.

## What's next for Enforce-BGP

We will try to incoporate Enforce-BGP with BGP2Vec to see how natural language processing power will do on our prediction of the anomalies. 

