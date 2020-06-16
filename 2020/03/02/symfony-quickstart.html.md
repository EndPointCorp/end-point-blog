---
author: "Árpád Lajos"
title: "Symfony Quickstart"
tags: symfony, php, webpack
gh_issue_number: 1597
---

<img src="/blog/2020/03/02/symfony-quickstart/symphony.jpg" alt="symphony" />
[Photo](https://unsplash.com/photos/VEOk8qUl9DU) by [Arindam Mahanta](https://unsplash.com/@arindam_mahanta)

This article is written for anyone who has experience working with PHP and is starting to work with Symfony. We won’t assume any prior knowledge you might have with Symfony, so if getting started with this framework is a high priority, then this article is for you. I know that it can be difficult and you may be unsure where to look; I was in the same situation when I first worked with Symfony.

You might be pointed to consult the [documentation](https://symfony.com/doc/current/index.html#gsc.tab=0), but even though the documentation is very detailed and nicely written, you might have a very urgent issue to solve, and thus not have time to read multiple articles about the framework before you start working. You might just need to quickly start, solve a few issues and worry about the details later.

### How do I run this stuff?

If your project does not exist yet, you will need to set up Symfony, using the steps nicely outlined in [Symfony’s setup guide](https://symfony.com/doc/current/setup.html).

Assuming that the project already exists and you need to quickly start working on it, you will need to run `composer install` in the root folder of the project to make sure that the dependencies are properly set. This could result in errors; for example, PHP might be not installed in your development environment. In this case, of course, you need to install PHP, which should not be a big problem if we continue to assume that you have some experience with PHP.

Another problem might be that Composer is not yet installed on your machine. If this is the case, install Composer by following the steps [here](https://getcomposer.org/download/).

You might be missing some PHP extensions at this point or have other problems. If so, read the error messages you get and solve them. If you don’t understand some error messages, don’t worry, you aren’t the first one struggling to make Symfony work. Search for the error message you got paired with the Symfony keyword and find others’ solutions.

### Composer

Composer is a server-side package manager which is frequently used by modern PHP applications. In the previous section we executed `composer install`. Let’s understand this command now. This command reads **composer.json**, resolves dependencies and installs them into the vendor folder.

If you intend to update to the latest versions of the dependencies outlined in **composer.lock**, run `composer update` or its alias `composer upgrade`.

There are two very important files to know about: **composer.json** and **composer.lock**. In **composer.json** the dependencies are specified as JSON. The actual value of a dependency is an expression to denote what kinds of versions are allowed. **composer.lock** specifies which dependencies should *not* be updated to the latest version and it contains the exact version number for the installed PHP packages, so if you have a **composer.lock** file and you want to fetch the latest versions allowed by **composer.json**, then you need to run `composer update`.

Since our article is just a quick start, we’ll avoid delving too deep into the realms of Composer, but if you want to learn more, it’s very well [documented](https://getcomposer.org/doc/03-cli.md). You’ll need an understanding of Composer to work on Symfony projects, but for the very short term you can get by with a minimal understanding.

Whenever you are pulling work done by others, you will need to make sure that the dependencies are updated. If there is any change in the downloaded **composer.json**, `composer install` should be executed. If you check out a different branch you should run `composer install` unless you are absolutely sure it’s not needed.

### Yarn

Yarn is a package manager which we can use to manage client-side packages if we choose to (Symfony does not enforce its use). If you already have a Node.js server installed, installing yarn is as simple as `sudo npm install -g yarn` with `-g` specifying a global installation. If you don’t have Node.js installed, it’s worth [downloading](https://nodejs.org/en/download/).

`yarn install` installs the dependencies of a project. You will need to run this (if Yarn is used in the project) when you first work with the project at least once, as well as whenever there’s a change in **package.json** (which serves the same purpose for Yarn as **composer.json** for Composer).

Consult Yarn’s [documentation](https://classic.yarnpkg.com/en/docs/) for more information.

### webpack

[webpack](https://webpack.js.org/) bundles client-side files. You can configure webpack to pack file content from a source location and send the packed content to a target location. Read more [here](https://symfony.com/doc/current/frontend/encore/simple-example.html#configuring-encore-webpack).

Encore can be restarted with `yarn run encore <env>`, which packs files into the target. However, this is unfriendly to the developer, because now each change in client-side code requires us running `yarn run encore <env>` to make sure that the newest client-side code will be used. This quickly becomes frustrating, since JavaScript and CSS, which never required deployment before, now need to be built. However, you can add the `--watch` switch like `yarn run encore <env> --watch` and from there on changes will be watched and detected, so you can be confident that client-side code will end up in the target path and you won’t have to worry about it.

The drawback, of course, is that this will eat up resources and will still be time consuming if the client-side code is very large. As a result, it is much smarter to just use the source path while in development mode. Sometimes browser caching will still cause us trouble while working this way, but a seasoned frontend developer is already used to that.

webpack is a nice tool and can be useful when used well, but it’s a good idea to limit its use. Avoiding webpack in development mode can be very helpful, allowing us to nicely debug and not worry about building client-side code. In production mode it adds a lot of value in obfuscating, minifying, and packing the code.

### MVC

<img src="/blog/2020/03/02/symfony-quickstart/mvc.svg" style="display: block; height: 300px; margin: auto" />

Model-View-Controller as a pattern is a standard for Symfony. Model means domain model, usually represented by entity and repository classes along with the business logic that uses them. View is the templating that eventually generates the HTML which will be served to the browser and displayed to the user. Controllers are the engines, the driving force, since the actions allowed to be performed can be found in them, putting everything together.

### Doctrine

[Doctrine](https://www.doctrine-project.org/projects/doctrine-orm/en/2.7/index.html) is an [ORM](https://en.wikipedia.org/wiki/Object-relational_mapping), which is very helpful in general for working with databases. Symfony does not enforce its use. You can use Flourishlib instead, or write your own queries. You can create an entity class (which represents a given table in the database) manually, but there is an automatic way to achieve that as well:

```
php bin/console make:entity
```

This will start a Q&A, which will be a discussion between the Symfony console and the programmer. After the programmer answers all the questions, the entity class will be generated. Typically these questions will be asked:

- Entity name
- Property names (until empty name is given)
  - Their field type
  - Their field length
  - Whether they are nullable

The documentation gives us a [very good example](https://symfony.com/doc/current/doctrine.html#creating-an-entity-class), resulting in:

```php
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

We notice a few things here. First of all, there is an annotation.

```php
/**
 * @ORM\Entity(repositoryClass="App\Repository\ProductRepository")
 */
```

This means that this entity has a repository class called `ProductRepository` in the namespace mentioned above.

```php
/**
 * @ORM\Id
 * @ORM\GeneratedValue
 * @ORM\Column(type="integer")
 */
```

This means that the `column` is of type `integer`, a `primary key`, and it’s a generated value. We notice that the `length` can be given as well. The data members are `private` and setters and getters are automatically generated.

The entity class is paired with a repository of its own, like:

```php
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

Note that it extends [ServiceEntityRepository](https://github.com/doctrine/DoctrineBundle/blob/master//Repository/ServiceEntityRepository.php). This offers quite a few features if we use it as a Doctrine repository. In the controller we can load a repository, like:

```php
$this->getDoctrine()->getRepository(Product::class)
```

You can search for objects via find, findBy or findOneBy, as described in the [API documentation](https://www.doctrine-project.org/api/orm/latest/Doctrine/ORM/EntityRepository.html). This way, we can load data from the database and use them as objects. Example:

```php
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

You can load a repository from within another by calling

```php
$this->getEntityManager()->getRepository("name")
```

However, in general I would suggest that repositories should not have interdependency. It’s far better in my opinion to have a business layer, a Service between the controller and the repository classes, which would combine different repositories’ operations if needed.

Getting or setting values of data members can be done via getters and setters very simply. As the [documentation](https://www.doctrine-project.org/projects/doctrine-orm/en/2.7/reference/working-with-objects.html) says, `persist` and `remove` are methods that notify the [Unit Of Work](https://www.programmingwithwolfgang.com/repository-and-unit-of-work-pattern/) that some write operations should occur, but the write operations are not executed yet at this point. The reason is simple: we may have multiple write operations to do and we might want to avoid doing them all as separate requests to the database, which might be on an entirely different machine on the other side of the globe. Requests to the database are costly operations and they accumulate. To avoid this, the application server first acknowledges what should be done, or, in other words, prepares some write operations. The `flush` method does the actual request sending for the write operations.

There is no ORM which solves everything, so sometimes we want to write our own scripts. We can of course do it, but Doctrine offers [DQL](https://www.doctrine-project.org/projects/doctrine-orm/en/2.7/reference/dql-doctrine-query-language.html) (Doctrine Query Language) as a compromise.

```php
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

You can apply entity changes upon the database via

```
php bin/console doctrine:migrations:migrate
```

Honestly I’m not very fond of changing the database schema based on entity classes; I consider this to be an anti-pattern, because we use a tool to generate a schema based on entities. Such a tool can have bugs or cause errors in the entities. It is much better to do it the other way around—that is, make a proper database schema, write SQL commands to change the schema whenever we need it and generate entity classes that way. Luckily Doctrine offers that feature as well:

```
php bin/console doctrine:mapping:import "App\Entity" annotation --path=src/Entity
```

Unfortunately it’s a trend to write entity classes and generate schema changes based on those, but that way we add a layer of complexity around schema planning, which should be as simple as possible. If something goes south with these migrations for any reason, that could result in very serious problems, while if we are to write schema-changing scripts in SQL rather than generating them from entity classes that we write (or generate), we at least have the means to acquire full understanding of what happens with the schema. Not everyone is a database specialist and most programmers are much more comfortable writing or even generating entity classes. But even if we generate them, it’s not much simpler in most cases than writing a small script which creates a table or alters it or drops it, so the objective gain from generating schema-changing scripts from entity classes is negligible at best.

On the other hand, the complex tool that we add is difficult to understand unless one delves into the actual code which generates the schema and the way the schema is generated is out of our hands, unless we are content with the current version of doctrine or accept the price of hacking into the code each time a new version is downloaded.

In short, my advice is to try to avoid generating schema changes based on entity classes whenever possible. We can always find exceptional cases, but in general, SQL is clearer than a tool that generates SQL.

### Controller

You can write or generate a controller. This is how you would generate one:

```
php bin/console make:controller <NamedController>
```

The command above will actually generate a controller class and ensure that it can be used in the project. Read more [here](https://symfony.com/doc/current/controller.html#generating-controllers).

You can generate a whole CRUD (support for Create, Read, Update, Delete features) for an entity via

```
php bin/console make:crud <YourEntity>
```

The documentation provides a simple example:

```php
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

```php
/**
 * @Route("/lucky/number/{max}", name="app_lucky_number")
 /*
```

The first parameter describes the path. Of course we can elaborate our routes more; let’s consider the example below:

```php
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

As we can see, we can specify which HTTP methods we support or even specify regular expressions for the URL parameters. Generating a URL is not difficult at all, one just needs to call `$this->generateURL`.

### Symfony and HTTP

As we could see earlier, Symfony actions are returning a Response. You can send JSON as Response, or even a JSONResponse, as the [documentation](https://symfony.com/doc/current/components/http_foundation.html#creating-a-json-response) describes. You can even specify a JSONP callback via

```php
$response->setCallback('handleResponse')
```

Don’t be afraid of this, it’s not very difficult and it’s well-documented.

Requests are also handled [nicely](https://symfony.com/doc/current/introduction/http_fundamentals.html):

```php
$request->query->get('id')
```

gets a GET parameter, while

```php
$request->request->get('category', 'default value')
```

is getting a post value.

```php
$request->query->all()
```

retrieves all GET parameters, while

```php
$request->request->all()
```

retrieves all POST parameters.

### Caching

Symfony supports caching through the Cache module, which, when switched on, will cache configuration and routes. If controller actions or routes are changed, then it is advisable to clear the cache via:

```
bin/console cache:clear && bin/console cache:warmup
```

Whether or not to switch on caching for your application at dev mode depends on the frequency of a need to cache cleanup. Read more [here](https://symfony.com/doc/current/cache.html).

### Configuration

Symfony configuration can be done via YAML, XML or PHP files. In the projects I have been working with, configuration was done in YAML files stored in the config folder inside the root folder of the project.

Inside the **src** folder we can find **Kernel.php** which glues together the project.

### Twig

Symfony is well-paired with Twig, a popular template engine. You might ask why we don’t use PHP for this purpose. We can use PHP or Smarty or other options for view templating, Twig is not required.

Using template engines instead of allowing the developers to use PHP as a template engine has the drawback of limiting the options. However, this could also be seen as a positive thing. Yes, it limits the options of the developers, but this way developers will not find it so easy and convenient to temporarily (?) implement their business logic as part of the view.

I’m okay with using PHP as a template engine as long as we do not mix up the layers of the application and by convention the view remains “only” the view. I’m also okay with using template engines, even though it is less convenient to use when we need to do some experimenting and code-writing for a very short time, after which it is reverted. In that kind of experimental work enforcing this separation is unnecessary bureaucracy, but the gain is that we will not have to deal with views with unnecessary implementations. So, this is a harmless form of bureaucracy, if such a thing exists.

### Summary

Symfony is a Framework which provides us with a way to work in conformity with the MVC pattern. Models are Entity classes along with their Repository pair, representing database tables, while Doctrine watches over the whole process, if used. Views are templates that generate HTML, for which Twig is a convenient tool, but you can use Symfony without relying on the usage of Twig. Configuration can be written in YAML, XML or PHP. PHP dependencies are handled by Composer, client-side dependencies can be handled by Yarn. Symfony has its own console that can be used to run different commands.

All in all, there are lots of features which Symfony offers, so using Symfony a good option to consider when planning a project. Getting started with Symfony can be difficult, but I hope this article will help you get started using Symfony in your projects.
