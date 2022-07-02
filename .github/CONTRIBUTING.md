# Contributing to python-valueserp

Some guidelines for contributing code to the python-valueserp to keep things clean
and consistent


## Using the issue tracker

The [issue tracker](https://github.com/joejoinerr/python-valueserp/issues)
is the preferred channel for bug reports, feature requests and submitting pull
requests.


## Pull requests

Pull requests - patches, improvements, new features - should remain focused in
scope and avoid containing unrelated commits. Please adhere to
[PEP 8](https://www.python.org/dev/peps/pep-0008/) as much as possible. 
Docstrings should follow the [Google styleguide](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings).

To submit a pull request:

1. Clone the repo, and configure the remotes:

   ```bash
   # Clone the repo into the current directory
   git clone https://github.com/joejoinerr/python-valueserp.git
   # Navigate to the newly cloned directory
   cd python-valueserp
   ```

2. Checkout the develop branch. If you cloned a while ago, get the latest 
   changes from upstream:

   ```bash
   git checkout develop
   git pull origin develop
   ```

3. Create a new feature branch (off the develop branch) to
   contain your feature, change, or fix:

   ```bash
   git checkout -b <feature-branch-name>
   ```

4. Commit your changes in logical chunks. Use Git's
   [interactive rebase](https://help.github.com/articles/about-git-rebase/)
   feature to tidy up your commits before publishing.

5. Locally rebase the upstream development branch into your topic branch:

   ```bash
   git pull --rebase origin develop
   ```

6. Push your topic branch up to the repo:

   ```bash
   git push origin <feature-branch-name>
   ```

7. [Open a Pull Request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request)
    with a clear title and description.
