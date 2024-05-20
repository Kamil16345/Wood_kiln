### Welcome on a repository dedicated to my Engineering Thesis
# A mock-up of a wood drying kiln 
## Controlled using Raspberry Pi and the AWS Cloud

It is a project that I've made from scratch and involved many areas of knowledge to finish it.

### What was the purpose of this project?
I wanted to create a fully maintainable mock-up of a wood dryer in appropriate scale to be able to carry out the process of drying the wood.  
The wood industry is a substantial part of the overall manufacturing sector. However, before wood can be subjected to further processing, it needs to be dried. The mockup I've developed enables users to dry a piece of wood, test the wood drying process, and then, if the tests are successful, transfer the process to a real dryer.  

## It has all started with a project in Inventor  
![image](https://github.com/Kamil16345/Wood_kiln/assets/75177619/404c728a-71b9-4907-afe2-ba00ea979918)

Then it turned into this: 

I designed a physical mock-up of a dryer, mounted electrical components, connected them to Raspberry Pi which is heart of this project  
and started collecting data from the periphery.  

I crafted a user interface to manually, from GUI level control every device like radiator, fan that is connected with dryer.  
The dryer is controlled wireless thanks to SSH protocol.  

I used **Python v.3.9.2** to develop a software for this product

Additionally, I decided to connect this project with AWS services to accumulate the data and visualize it to be available worldwide to keep track of it.  
## AWS Services that I used:
* IoT Core,
* Lambda,
* DynamoDB,
* Athena,
* QuickSight

### Live demo:  
https://www.youtube.com/watch?v=RiVlgQARXeY
