---
author: "Lajos Árpád"
title: "Symfony quickstart"
tags: symfony, php, composer, doctrine, yarn, twig

---

This article is written for anyone who has experience working with PHP and starts to work with Symfony. Here we do not assume any prior knowledge that you might have with Symfony, so, if being able to start very quickly with this Framework is of high priority, then this article is written for you. I know that it’s difficult and one may be unsure where to look, I was in this specific situation when I first worked with Symfony.

Yes, you might be pointed to consult the [documentation](https://symfony.com/doc/current/index.html#gsc.tab=0), but even though the documentation is very detailed and nicely written, you might have a very urgent issue to solve, so you might be physically unable to read multiple articles about the framework before you start working. You might just need to quickly start, solve a few issues and to worry about the details later.

## How to run this stuff?

If your project does not exist yet, then you will need to set up Symfony, then you will need to go through the steps nicely written in the [article](https://symfony.com/doc/current/setup.html) about this.

Assuming that the project already exists and you need to quickly start working on it, you will need to run

```
composer install
```

in the root folder of the project to make sure that the dependencies are properly set. Naturally, this might result in errors, for example PHP might be not installed on your dev env. In this case, of course, you need to install PHP, which should not be a big problem if we continue to assume that you already have some experience with PHP. Another problem might be that Composer is not installed yet on your machine. If that’s the case, then of course composer install will fail. Make sure that Composer is available for you, by following [the steps the official documentation of Composer suggests](https://getcomposer.org/download/) if needed.

You might be missing some PHP extensions at this point or have other problems. If that’s the case, then read the error messages that you might get and solve them. If you do not understand some error messages, don’t worry, you will not be the first one struggling to make Symfony work, search for the exact same error message paired with the Symfony keyword and see what the solution was for others.

## Composer

Composer is a server-side package manager which is frequently used by modern PHP applications. In the previous section we have executed ```composer install```, let’s understand this command now. This command reads **composer.json**, resolves dependencies and installs them into the vendor folder.

If you intend to update to the latest versions of the dependencies outlined in **composer.lock**, run

```
composer update
```

or its alias

```
composer upgrade
```

There are two very important files to know about: **composer.json** and **composer.lock**. In **composer.json** the dependencies are specified as JSON, the actual value of a dependency is an expression to denote what kinds of versions are allowed. **composer.lock** specifies which dependencies should not be updated to the latest version and it contains the exact version number for the installed PHP packages, so, if you have a **composer.lock** file and you want to fetch the latest versions allowed by **composer.json**, then you need to run ```composer update```.

Since our article is a quick start, we avoid delving too deeply into the realms of Composer, because one may need to work on the project first, but it’s very nicely [documented](https://getcomposer.org/doc/03-cli.md). One needs to have an understanding of Composer in order to work on Symfony projects, but for the very short term one can acquire just a minimal understanding in order to quickly start working.

Whenever you are pulling work done by others, you will need to make sure that the dependencies are updated. If there is any change in **composer.json** that you download, then ```composer install``` should be executed. If you check out to a different branch then you should run ```composer install``` unless you are absolutely sure that it’s not needed.

## Yarn

Yarn is a package manager which we can use in order to manage client-side packages. If one already has a NodeJS server installed, then installing yarn is as simple as

```
sudo npm install -g yarn
```

That ```-g``` means globally. If one does not have NodeJS yet, then it’s worth [downloading](https://nodejs.org/en/download/) it.

```
yarn install
```

installs the dependencies of a project. You will need to run this (if Yarn is used in the project) when you first work with the project at least once. Whenever there is a change in **package.json** (that serves the same purpose for Yarn as **composer.json** for Composer), you will need to run ```yarn install```.

You may consult the [documentation](https://classic.yarnpkg.com/en/docs/) of Yarn for more information.

## Webpack

[Webpack](https://webpack.js.org/) is responsible for bundling the client-side files. One may configure webpack to pack file content from a source location and bring the packed content into a target location. [Read more](https://symfony.com/doc/current/frontend/encore/simple-example.html#configuring-encore-webpack).

Encore can be restarted via

```
yarn run encore <env>
```

and thus files are packed into the target. However, this is unfriendly towards the developer, because now each change in client-side code requires us running ```yarn run encore <env>``` to make sure that the newest client-side code will be used. One will quickly become frustrated, seeing that Javascript and CSS, which never required a deployment before, now are to be built. However, one can add the ```--watch``` runtime parameter, like

```
yarn run encore <env> --watch
```

and from there on, changes will be watched and detected, so one can be confident that client-side code will end up in the target path and will not have to be worried about it.

The drawback, of course, is that this will eat up resources and will still be time-consuming if the client-side code is very large. As a result, it is a much smarter way to organize code to just use the source path while in development mode. Sometimes browser cache will still cause us trouble while working this way, but a seasoned frontend developer is already used to that.

Webpack is a nice tool and it can be used in a very wise manner but it is a good idea to limit its use wisely. Avoiding its usage in development mode could be very helpful, allowing us to nicely debug and not worry about building client-side code. In prod mode it adds a lot of value in obfuscating, minimising and packing the code.

## MVC

<div style="width: 100%; text-align: center;"><img src="/blog/2020/02/21/symfony-quickstart/mvc.png"></div>

Image taken from [tutorialspoint](https://www.tutorialspoint.com/mvc_framework/mvc_framework_introduction.htm).

Model-View-Controller, as a pattern is a standard for Symfony. Controllers are the engines, the driving force, since the actions allowed to be performed can be found in them, putting everything together. Model is domain model, usually represented by entity and repository classes along with the business logic that uses them. View is the templating that eventually generates the HTML which will be served to the browser so it can display it to the user.

## Doctrine

[Doctrine](https://www.doctrine-project.org/projects/doctrine-orm/en/2.7/index.html) is an ORM, which is very much helpful in general for working with databases. Symfony does not enforce its use. One may use Flourishlib instead, or write his/her own queries. One can create an entity class (which represents a given table in the database) manually, but there is an automatic way to achieve that as well:

```
php bin/console make:entity
```

This will start a Q&A, which will be a discussion between Symfony console and the programmer. After the programmer answers all the asked questions, the entity class will be generated. Typically these questions will be asked:

- Entity name
- Property names (until empty name is given)
    - Their field type
    - Their field length
    - Whether they are nullable

The documentation gives us a [very good example](https://symfony.com/doc/current/doctrine.html#creating-an-entity-class), resulting in:

```
// src/Entity/Product.php
namespace App\Entity;

use Doctrine\ORM\Mapping as ORM;

/**
 * @ORM\Entity(repositoryClass="App\Repository\ProductRepository")
 */
class Product
{
    /**
     * @ORM\Id
     * @ORM\GeneratedValue
     * @ORM\Column(type="integer")
     */
    private $id;

    /**
     * @ORM\Column(type="string", length=255)
     */
    private $name;

    /**
     * @ORM\Column(type="integer")
     */
    private $price;

    public function getId()
    {
        return $this->id;
    }

    // ... getter and setter methods
}
```

We can notice a few things here. First of all, that there is an annotation.

```
/**
 * @ORM\Entity(repositoryClass=”App\Repository\ProductRepository”)
 */
```

means that this entity class has a [repository](https://en.wikipedia.org/wiki/Software_repository) class called ```ProductRepository``` in the namespace mentioned above.

```
/**
 * @ORM\Id
 * @ORM\GeneratedValue
 * @ORM\Column(type=”integer”)
 */
```

Means that the ```column``` is ```integer```, a ```primary key``` and it’s generated. We can notice that the ```length``` can be given as well. The data members are ```private``` and setters and getters are automatically generated.

The entity class is paired with a repository of its own, like:

```
namespace App\Repository;

use App\Entity\Product;
use Doctrine\Bundle\DoctrineBundle\Repository\ServiceEntityRepository;
use Doctrine\Persistence\ManagerRegistry;

class ProductRepository extends ServiceEntityRepository
{
    public function __construct(ManagerRegistry $registry)
    {
        parent::__construct($registry, Product::class);
    }
}
```

Note that it extends [ServiceEntityRepository](https://github.com/doctrine/DoctrineBundle/blob/master//Repository/ServiceEntityRepository.php). This offers quite a lot of features if we use it as a Doctrine repository. In the controller we can load a repository, like:

```
$this->getDoctrine()->getRepository(Product::class)
```

One can search for objects via find, findBy or findOneBy, as described in the [API documentation](https://www.doctrine-project.org/api/orm/latest/Doctrine/ORM/EntityRepository.html). This way, we can load data from the database and use them as objects. Example:

```
$repository = $this->getDoctrine()->getRepository(Product::class);

// look for a single Product by its primary key (usually "id")
$product = $repository->find($id);

// look for a single Product by name
$product = $repository->findOneBy(['name' => 'Keyboard']);
// or find by name and price
$product = $repository->findOneBy([
    'name' => 'Keyboard',
    'price' => 1999,
]);

// look for multiple Product objects matching the name, ordered by price
$products = $repository->findBy(
    ['name' => 'Keyboard'],
    ['price' => 'ASC']
);

// look for *all* Product objects
$products = $repository->findAll();
```

In general, the criteria to search by is an array of key-value pairs. The same can be said about sorting.

One can load a repository from within another by calling

```
$this->getEntityManager()->getRepository(“name”)
```

However, in general I would suggest that repositories should not have interdependency. It’s far better in my opinion to have a business layer, a Service between the controller and the repository classes, which would combine different operations of different repositories if needed.

Getting or setting values of data members can be done via getters and setters in a very simple manner. As the [documentation](https://www.doctrine-project.org/projects/doctrine-orm/en/2.7/reference/working-with-objects.html) says, ```persist``` and ```remove``` are methods that notify the [Unit Of Work](https://www.programmingwithwolfgang.com/repository-and-unit-of-work-pattern/) that some write operations should occur, but the write operations are not executed yet at this point. The reason is simple: we may have multiple write operations to do and we might want to avoid doing them all as separate requests to the database, which might be on an entirely different machine at the other side of the globe behind a network. Requests to the database are costly operations and they accumulate. To avoid this, the application server first acknowledges what should be done, or, in other words, prepares some write operations. The ```flush``` method does the actual request sending for the write operations.

There is no ORM which solves everything, sometimes we want to write our own scripts. We can of course do it, but Doctrine offers [DQL](https://www.doctrine-project.org/projects/doctrine-orm/en/2.7/reference/dql-doctrine-query-language.html) (Doctrine Query Language) as a compromise.

```
<?php
$query = $em->createQuery('SELECT u FROM ForumUser u WHERE (u.username = :name OR u.username = :name2) AND u.id = :id');
$query->setParameters(array(
    'name' => 'Bob',
    'name2' => 'Alice',
    'id' => 321,
));
$users = $query->getResult(); // array of ForumUser objects
```

The example above is a parameterized query, where we search by username and id, without knowing what the actual filter values are at the time of development. These values are determined at runtime.

One can apply entity changes upon the database via

```
php bin/console doctrine:migrations:migrate
```

Honestly I’m not very fond of changing the database schema based on entity classes, I consider this to be an anti-pattern, because we use a tool to generate a schema based on entities. Such a tool can have bugs, or, we might have errors in the entities. It is much better to do it the other way around, that is, make a proper database schema, write SQL commands to change the schema whenever we need it and generate entity classes that way. Luckily Doctrine offers that feature as well:

```
php bin/console doctrine:mapping:import "App\Entity" annotation --path=src/Entity
```

Unfortunately it’s a trend to write entity classes and generate schema changes based on those, but that way we add a layer of complexity around schema planning, which should be as simple as possible. If something goes south with these migrations for any reason, that could result in very serious problems, while if we are to write schema-changing scripts in SQL rather than generating them from entity classes that we write (or generate), then we at least have the means to acquire full understanding of what happens with the schema. Not everyone is a database specialist and most of the programmers are much more comfortable in writing or even generating entity classes, but even if we generate them, it’s not much simpler in most cases than writing a small script which creates a table or alters it or drops it, so the objective gain from generating schema-changing scripts from entity classes is negligible at best.

On the other hand, the complex tool that we add is difficult to understand unless one delves into the actual code which generates the schema and the way the schema is generated is out of our hands, unless we are content with the current version of doctrine or accept the price of hacking into the code each time a new version is downloaded.

In short, my advice is to try to avoid generating schema changes based on entity classes whenever possible. We can always find exceptional cases, but in general, SQL is clearer than a tool that generates SQL.

## Controller

One can write or generate a controller. This is how one can generate one:

```
php bin/console make:controller <NamedController>
```

The command above will actually generate a controller class and ensure that it can be used in the project. Read more [here](https://symfony.com/doc/current/controller.html#generating-controllers).

One can generate a whole CRUD for an entity via

```
php bin/console make:crud <YourEntity>
```

The documentation provides a simple example:

```
// src/Controller/LuckyController.php
namespace App\Controller;

use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;

class LuckyController
{
    /**
     * @Route("/lucky/number/{max}", name="app_lucky_number")
     */
    public function number($max)
    {
        $number = random_int(0, $max);

        return new Response(
            '<html><body>Lucky number: '.$number.'</body></html>'
        );
    }
}
```

Note that there is annotation for this controller:

```
/**
 * @Route(“/lucky/nunmber/{max}”, name=”app_lucky_number”)
 /*
```

The first parameter describes the path. Of course we can elaborate our routes more, let’s consider the example below:

```
namespace App\Controller;

use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;

class MyController extends AbstractController
{
    /**
     * @Route("/home")
     */
    public function home()
    {
        return new Response("home",  Response::HTTP_OK,
            ['content-type' => 'text/plain']);
    }

    /**
     * @Route("/about", methods={"GET", "POST"})
     */
    public function about(Request $request)
    {
        $method = $request->getRealMethod();
        $msg = "about: " . $method;

        return new Response($msg,  Response::HTTP_OK,
            ['content-type' => 'text/plain']);
    }    

    /**
     * @Route("/news/{id}", requirements={"page"="\d+"})
     */
    public function news($id)
    {
        $msg = 'News ' . $id;

        return new Response($msg,  Response::HTTP_OK,
            ['content-type' => 'text/plain']);
    }    
}
```

Code taken from [zetcode.com](http://zetcode.com/symfony/routeannotation/).

As we can see, we can specify what HTTP methods we support or even specify regular expressions for the URL parameters. Generating a URL is not difficult at all, one just needs to call ```$this->generateURL```.

## Symfony and HTTP

As we could see earlier, Symfony actions are returning a Response. One can send a JSON as Response, or even a JSONResponse, as the [documentation](https://symfony.com/doc/current/components/http_foundation.html#creating-a-json-response) describes. One can even specify a JSONP callback via

```
$response->setCallback(‘handleResponse’)
```

Don’t be afraid of this, it’s not very difficult and it’s well-documented.

Requests are also handled [nicely](https://symfony.com/doc/current/introduction/http_fundamentals.html),

```
$request->query->get(‘id’)
```

gets a  GET parameter, while

```
$request->request->get(‘category’, ‘default value’)
```

is getting a post value.

```
$request->query->all()
```

retrieves all GET parameters

```
$request->request->all()
```

retrieves all POST parameters.

## Caching

Symfony supports caching with the caching module, which, if switched on will cache configuration and routes. If controller actions or routes are changed, then it is advisable to clear the cache via

```
bin/console cache:clear && bin/console cache:warmup
```

Whether or not to switch on caching for your application at dev mode depends on the frequency of a need to cache cleanup. Read more [here].

## Configuration

Symfony configuration can be done via YAML, XML or PHP files. In the projects I have been working with, configuration was done in YAML files and they were stored in the config folder inside the root folder of the project.

Inside the **src** folder we can find **Kernel.php** which glues together the project.

## Twig

Symfony is well-paired with Twig, a popular template engine. Why don’t we use PHP for this purpose, one might ask. The answer is that we can use PHP or Smarty or whatever we intend to use for view templating, nobody forces us to use Twig.

Using template engines instead of allowing the developers to use PHP as a template engine has the drawback of limiting the options, however, the exact reason they are used, especially by large teams is the exact same thing that we can outline as its drawback. Yes, it limits the options of the developers, but this way developers will not find it so easy and convenient to temporarily (?) implement their business logic as part of the view.

If my opinion matters, I’m okay with using PHP as a template engine as long as we do not mix up the layers of the application and, by convention the view will remain “only” the view. I’m also okay with using template engines, even though it is less convenient to use when we need to do some experimenting and writing some code for a very short time, after which it is reverted. In that kind of experimental work one feels that enforcing this separation is unnecessary bureaucracy, but the gain is that we will not have to deal with views where lots of things are implemented which should not be there. So, this is a harmless form of bureaucracy, if such a thing exists.

## Summary

Symfony is a Framework which provides us with a way to work in conformity with the MVC pattern. Models are Entity classes along with their Repository pair, representing database tables, while Doctrine watches over the whole process, unless one chooses not to use Doctrine. Views are templates that generate HTML, for which Twig is a convenient tool, but one can use Symfony without relying on the usage of Twig. Configuration can be written in YAML, XML or PHP. PHP dependencies are handled by Composer, client-side dependencies are handled by Yarn. Symfony has its own console that can be used to run different commands.

All in all, there are lots of features which Symfony offers, so using Symfony is definitely an option to consider when planning a project, but if someone just starts to work using Symfony, then the initial period might be more difficult. This article aims to reduce this difficulty.
