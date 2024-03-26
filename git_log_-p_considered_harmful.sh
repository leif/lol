#!/bin/bash
set -e
dir=$(mktemp -d)
cd $dir
git init --initial-branch branch_one
git config --local user.name Name
git config --local user.email email@example.com
echo value_one > foo
git add foo
git commit -m one
git checkout -b branch_two
echo value_two > foo
git commit -am two
git checkout branch_one
git merge --no-ff --no-commit branch_two
echo value_three > foo
git add foo
git commit -m 'merge branch_two into branch_one

This commit changes the contents of the file "foo" to
"value_three", but this change does not appear in the output
git log -p unless you use specify a value for --diff-merges
or use the --first-parent option.'
echo "

Here is git log -p:
===================
"
git --no-pager log -p
echo "

Here is git log -p --first-parent:
==================================
"
git --no-pager log -p --first-parent
rm -rf $dir
