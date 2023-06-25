# Final-Project
DOLORES: Deep Contextualized Knowledge Graph Embeddings -> Node2Vec

This code is for the GUI for the Final Project
Created by Evgeny Vexler and Saar Keshet
*Note: check the paths and the names of the files.*

In the folder dist/FinalProject, you can find an exe file to run the program.

## ***Training Part:***

In the submission folder, you can find the book and the presentation
In addition, there is a Node2Vec Link Prediction.ipynb notebook for google collab
to train the model on the dataset use the notebook and load it to your collab.
the dataset should be in this format:

![image](https://github.com/Saark07/Final-Project/assets/80771666/f1a54d11-12f8-4c80-b99b-614a8b27db4b)

Fig1: Dataset that shows a connection between nodes.

and to run the GUI a CSV file containing IDs and names of the academic papers is required In this format:

![image](https://github.com/Saark07/Final-Project/assets/80771666/712e9236-ac55-446a-9236-b7f970b3ffe1)

Fig2: Dataset that contains IDs and names of the academic papers.


after the training is finished there are 2 output files:
1) cora_graph.gexf
2) reconstructed_edges.csv
reconstructed_edges.csv will be in this format:

![image](https://github.com/Saark07/Final-Project/assets/80771666/d2ee7d03-d8a4-4577-942f-235dd2553a4b)

Fig3: The training results, represents the number of times each edge was reconstructed.

## ***GUI part:***

*Some requirements may be needed, open the terminal and enter: pip install PyQt5*

**Note there might be additional installations*

1) Home Page:
   ![image](https://github.com/Saark07/Final-Project/assets/80771666/3e34f97b-2c2a-4d2a-9985-dd01b0570fd8)

2) Loading Dataset select (Fig2) dataset
3) Load Trained Data select (Fig3) dataset
4) Click Next (might take time, depending on the dataset size) and Search for a paper

   ![image](https://github.com/Saark07/Final-Project/assets/80771666/7a9d4e54-3d21-47db-a89a-d6ea7764e1cb)

5) Results:

![image](https://github.com/Saark07/Final-Project/assets/80771666/e02c22de-f1b4-4795-baa7-0820c4c7ef3b)




