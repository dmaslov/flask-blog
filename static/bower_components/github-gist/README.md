# &lt;github-gist&gt;

A [Polymer](http://polymer-project.org) element for displaying github [gists](https://gist.github.com)

## Demo

> [Check it live](http://dmaslov.github.io/github-gist).

## Installation

Install using [Bower](http://bower.io):

```shell
 bower install github-gist
```

## Usage

* Import Web Components' polyfill:

```
<script src="bower_components/platform/platform.js"></script>
<script src="bower_components/polymer/polymer.js"></script>
```

* Import Custom Element:

```
<link rel="import" href="bower_components/github-gist/github-gist.html">
```

* Start using it!

```
<github-gist gistid="e54a2ed1b12934d3e134"></github-gist>
```

## Options

Attribute  | Options                   | Default             | Description
---        | ---                       | ---                 | ---
`gistid`      | *string*                  | ``                  | id of gist that will be loaded


## Examples:

```
<github-gist gistid="e54a2ed1b12934d3e134"></github-gist>
```
## License

[MIT License](http://opensource.org/licenses/MIT)
