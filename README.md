# Badger

A python script to add badges to all the accessible repos for a given Github token.


## Use Case:
As the pieces we work upon grow, so does number of repos we touch on github. With this comes a problem of updating something across all the repos.
With this script you will be able to add badges at one go without hassle of any manual task.

## Requirement:
 - Github Token
 - Python3
 
 ![](assets/access_token_generator.gif)
  
## Dependencies
 - `PyInquirer`
 - `requests`

 > `make` command will install the dependencies by itself.

## Usage
```
$make
```
 ![](assets/add_badges.gif)

## Supported badges

As of now this supports:
 1. visitors
 1. code-size.
 
## Stats
![visitors](https://visitor-badge.glitch.me/badge?page_id=jayeshathila.badger)	![code-size](https://img.shields.io/github/languages/code-size/jayeshathila/badger)
