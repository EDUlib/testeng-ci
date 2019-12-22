"""
Script to help create a PR. To be run by
a Jenkins job that cleans up python code base
"""
import click

from jenkins.github_helpers import CODE_CLEANUP_BRANCH_NAME
from jenkins.pull_request_creator import PullRequestCreator


@click.command()
@click.option(
    '--sha',
    help="Sha of the merge commit to base the new PR off of",
    required=True,
)
@click.option(
    '--repo_root',
    help="Path to local repository to run make upgrade on. "
         "Make sure the path includes the repo name",
    required=True,
)
@click.option(
    '--user_reviewers',
    help="Comma separated list of Github users to be tagged on pull requests",
    default=None
)
@click.option(
    '--team_reviewers',
    help="Comma separated list of Github teams to be tagged on pull requests",
    default=None
)
@click.option(
    '--packages',
    help="Comma separated list of python packages installed for the cleanup job",
    default=None
)
@click.option(
    '--scripts',
    help="Comma separated list of scripts/commands executed for the cleanup job",
    default=None
)
# pylint: disable=missing-function-docstring
def main(sha, repo_root, user_reviewers, team_reviewers, packages, scripts):
    scripts = "\n".join(scripts.split(','))
    packages = "\n".join(packages.split(','))
    message = (
        "Python code cleanup by the cleanup-python-code Jenkins job.\n" +
        "\n" +
        "This pull request was generated by the cleanup-python-code Jenkins job, which ran\n" +
        "{0}\n" +
        "\n" +
        "The following packages were installed:\n" +
        "{1}"
    ).format(scripts, packages)

    pull_request_creator = PullRequestCreator(sha=sha, repo_root=repo_root, branch_name=CODE_CLEANUP_BRANCH_NAME,
                                              user_reviewers=user_reviewers, team_reviewers=team_reviewers,
                                              commit_message=message, pr_title="Python Code Cleanup",
                                              pr_body=message)

    pull_request_creator.create(delete_old_pull_requests=False)


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter