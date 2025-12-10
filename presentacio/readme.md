- Carles Matoses

# Questions for first session:
- Burger Charts: A Quantitative Display of Set Intersections

Overall is a concise and simple paper that explains a novel Chart for analysing interaction between words. Two questions that may provide future improvement:

  - In the paper, they Simply create sets from the words in the same text but with this strategy we loose contextual relations within words. For example, we are analysing the "abortion" item in a dataset. We want to separate a burger in two sections "PRO" and "AGAINST" abortion to see if item "cancer" is only used for arguments against "abortion". For this we could use some AI for contextual analysis of the database for classification and add additional functionality to split columns based on flags. Are there any plans for expanding functionality in contextual directions? sentence relation, paragraph relations, positive or negative usage of the words, causation-correlation, ...

  - On the same direction of questions, how is it  handled polysemy or keywords that appear in different senses within the same document?


# Questions for second session:

- Area-adaptive Drawing of Rooted Trees

  - Can the method be extended to draw orthogonal trees or radial trees with area-adaptive behavior? It says in the paper there are only two connections to the leaf, either left or top. So I assume it will be reuqired to modify the wiring method to do so. Is it compex to do?

  - This question may be out of the scopes but, in the conclusion they mention that further studies should explore time reduction on the computation part. In the paper they do not show any example of "time" in seconds of how much it costs. I understand that depending on the hardware we get different results but I dont have any perception of how much seconds it is costing for a 1000 loops for example. Do you have an aproximate idea of how much time is it taking? also, is there any room for paralelization? even gpu usage? or it can only be done in sequential? 