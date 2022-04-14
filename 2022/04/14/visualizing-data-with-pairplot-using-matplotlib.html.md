---
author: "Kursat Aydemir"
title: "Visualizing Data with Pair-Plot Using Matplotlib"
tags: python, matplotlib, data visualization, plot, data science
---

![dfsdfsdfsdfs](/blog/2022/04/14/pexels-sebastian-361530.jpg")

Photo by Sebastian: https://www.pexels.com/photo/gray-wallpaper-361530/


## Pair Plot

When we say pair-plot it means plotting "pairwise relationships in a dataset" ([seaborn.pairplot](https://seaborn.pydata.org/generated/seaborn.pairplot.html)). There are a few well-known visualization modules of `python` that widely used by data scientists and analysts: [matplotlib](https://matplotlib.org/) and [seaborn](https://seaborn.pydata.org/). I know I didn't mention many others as well but these are kind of defacto guys. In the sense of level we can consider `matplotlib` as the more primitive library and `seaborn` "is a Python data visualization library based on [matplotlib](https://matplotlib.org/). It provides a high-level interface for drawing attractive and informative statistical graphics" ([seaborn](https://seaborn.pydata.org/)).

Seaborn's higher level pre-built plot functions provide us a good practice. Pair-Plot is one of them. With `matplotlib` you can plot many plot types like line, scatter, bar, histograms and so on. Pair-plot is a plotting model rather than a plot type individually. Here is a pair-plot example depicted on `seaborn` site.

![Seaborn pairplot](/blog/2022/04/14/pairplot_3_0.png)
Figure 1: Seaborn pairplot

Using a pair-plot we aim to visualize the correlation of each feature pair in a dataset against the class distribution. The diagonal of the pairplot is different than the other pairwise plots as you see in Figure 1. That is because the diagonal plots are rendering for the same feature pairs. So we wouldn't need to plot the correlation of the feature in the diagonal. Instead we can just plot the class distribution for that pair using one kind of plot type. The different feature pair plots are usually kind of scatter plot or sometimes can be heatmaps so that the class distribution makes sense in terms of correlation. Also the the plot type of diagonal can be chosen among the mostly used kind of plots such as histogram, KDE (kernel density estimate) which essentially plots the density distribution of the classes.

Since `pair-plot` visually gives an idea of correlation of each feature pair, it helps us to understand and quickly analyse the `correlation matrix` (Pearson) of the dataset as well.

## Custom Pair-Plot using Matplotlib

Since `matplotlib` is a relatively primitive and doesn't provide ready to use pair-plot function we can do it ourselves in a similar way `seaborn` does. You normally won't necessarily create such home-made functions if they are already available in modules like `seaborn`. But you'd want to implement your visualization methods in a custom way would give you a chance to know what you plot and may be sometimes in a very different than the existing ones. But I am not going to introduce an exceptional case here but creating our pair-plot grid using `matplotlib`.

### Plot Grid Area

Initially we need to create a grid plot area using `subplots` function of `matplotlib` like below.

```Python
fig, axis = plt.subplots(nrows=3, ncols=3)
```

For a pair-plot grid you should give the same row and column size because we are going to plot pairwise. Now we can prepare plot function for the plot grid area we created. If we have 3 features in our dataset as this example we can loop through the features per feature like below.

```Python
for i in range(0, 3):
    for j in range(0, 3):
        plotPair()
```

For cleaner code it is better to move the single pair plotting in another function. Below is a function I previously created for one of my courseworks assignments (in Dec. 2021, UoL). Plotting a single pair in a grid needs to get the current axis for the current grid cell and identify the current feature data values to on the current axis. Another thing to consider is where to render the labels of axes. If we were plotting a single chart it would be easy to render the labels on each axis of the chart. But in a pair plot it is better to plot the labels on the left-most and bottom-most of the grid area so that we won't bother the inner subplots with the dirty labeling.

```Python
def plot_single_pair(ax, feature_ind1, feature_ind2, _X, _y, _features, colormap):
    """Plots single pair of features.

    Parameters
    ----------
    ax : Axes
        matplotlib axis to be plotted
    feature_ind1 : int
        index of first feature to be plotted
    feature_ind2 : int
        index of second feature to be plotted
    _X : numpy.ndarray
        Feature dataset of of shape m x n
    _y : numpy.ndarray
        Target list of shape 1 x n
    _features : list of str
        List of n feature titles
    colormap : dict
        Color map of classes existing in target

    Returns
    -------
    None
    """

    # plot distribution histogram if the features are the same (diagonal of the pair-plot)
    if feature_ind1 == feature_ind2:
        tdf = pd.DataFrame(_X[:, [feature_ind1]], columns = [_features[feature_ind1]])
        tdf['target'] = _y
        for c in colormap.keys():
            tdf_filtered = tdf.loc[tdf['target']==c]
            ax[feature_ind1, feature_ind2].hist(tdf_filtered[_features[feature_ind1]], color = colormap[c], bins = 30)
    else:
        # other wise plot the pair-wise scatter plot
        tdf = pd.DataFrame(_X[:, [feature_ind1, feature_ind2]], columns = [_features[feature_ind1], _features[feature_ind2]])
        tdf['target'] = _y
        for c in colormap.keys():
            tdf_filtered = tdf.loc[tdf['target']==c]
            ax[feature_ind1, feature_ind2].scatter(x = tdf_filtered[_features[feature_ind2]], y = tdf_filtered[_features[feature_ind1]], color=colormap[c])

    # print the feature labels only on the left side of the pair-plot figure
    # and bottom side of the pair-plot figure. 
    # Here avoiding to print the labels for inner axe plots.
    if feature_ind1 == len(_features) - 1:
        ax[feature_ind1, feature_ind2].set(xlabel=_features[feature_ind2], ylabel='')
    if feature_ind2 == 0:
        if feature_ind1 == len(_features) - 1:
            ax[feature_ind1, feature_ind2].set(xlabel=_features[feature_ind2], ylabel=_features[feature_ind1])
        else:
            ax[feature_ind1, feature_ind2].set(xlabel='', ylabel=_features[feature_ind1])

```

Let's go back to the initial plotting of the grid area and adjust the call of `plot_single_pair` function. We can adjust figure size of the grid area using `fig.set_size_inches` depending on the feature count so that we can prepare a well scaled area.

```Python
    colormap={0: "red", 1: "green", 2: "blue"}

    fig.set_size_inches(feature_count * 4, feature_count * 4)

    # iterate through features to plot pairwise
    for i in range(0, 3):
        for j in range(0, 3):
            plot_single_pair(axis, i, j, X, y, features, colormap)

    plt.show()
```

In my `plot-single_pair` function notice that I also used a `colormap` `dictionary`. This dictionary is used to color the classes (labels) of the dataset to distinguish in a scatter plot or a histogram and makes it look more beautiful.

Here is my final grid plot function for pair-plot:

```
def myplotGrid(X, y, features, colormap={0: "red", 1: "green", 2: "blue"}):
    """Plots a pair grid of the given features.

    Parameters
    ----------
    X : numpy.ndarray
        Dataset of shape m x n
    y : numpy.ndarray
        Target list of shape 1 x n
    features : list of str
        List of n feature titles

    Returns
    -------
    None
    """

    feature_count = len(features)
    # create a matplot subplot area with the size of [feature count x feature count]
    fig, axis = plt.subplots(nrows=feature_count, ncols=feature_count)
    # setting figure size helps to optimize the figure size according to the feature count.
    fig.set_size_inches(feature_count * 4, feature_count * 4)

    # iterate through features to plot pairwise
    for i in range(0, feature_count):
        for j in range(0, feature_count):
            plot_single_pair(axis, i, j, X, y, features, colormap)

    plt.show()
```


### Pair-Plot a Dataset

Let's now prepare a dataset and plot using our custom pair-plot implementation. Notice in that in my `plot_single_pair` function I passed the feature and target values as `numpy.ndarray` type.

Let's get `iris` dataset from `SciKit-Learn` dataset collection and do a quick exploratory data analysis..

```
from sklearn import datasets
iris = datasets.load_iris()
```

Here are the targets (classes) of iris dataset:

```
iris.target_names
array(['setosa', 'versicolor', 'virginica'], dtype='<U10')
```

And here we can see the feature names and a few lines of the dataset values.

```
iris_df = pd.DataFrame(iris.data, columns = iris.feature_names)
iris_df.head()
```

<table>
<tr><td></td><td>sepal length (cm)</td><td>sepal width (cm)</td><td>petal length (cm)</td><td>petal width (cm)</td><tr>
<tr>
<td>0</td><td>5.1</td><td>3.5</td><td>1.4</td><td>0.2</td>
</tr>
<tr>
<td>1</td><td>4.9</td><td>3.0</td><td>1.4</td><td>0.2</td>
</tr>
</table>

Since `iris.data` and `iris.target` are already of `numpy.ndarray` as I implemented in my function I don't need any further dataset manipulation here. Now let's finally call `myplotGrid` function and render the pair-plot for `Iris` dataset.

Note that you can change color per target in `colormap` as you wish.

```
myplotGrid(iris.data, iris.target, iris.feature_names, colormap={0: "red", 1: "green", 2: "blue"})
```

And here is my custom pair-plot output:

![Pair-Plot output](/blog/2022/04/14/pairplot-output.png)


For further research I encourage you to go and do your exploratory data analysis and take a look at the correlation coefficient analysis to get more insights for pair-wise analysis.
