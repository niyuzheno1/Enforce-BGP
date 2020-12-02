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

In process

## Accomplishments that I'm proud of

In process

## What I learned

In process

## What's next for Enforce-BGP

We will try to incoporate Enforce-BGP with BGP2Vec to see how natural language processing power will do on our prediction of the anomalies. 

