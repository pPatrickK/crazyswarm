The crazyswarm git repository uses submodules. For detailed information, read https://git-scm.com/book/en/v2/Git-Tools-Submodules.

In short:
1. Whenever you have changed somthing in one of the submodules, you have to commit/push to the submodule repository, and additionally tell the main-repository that another commit of the submodule should be used (add/stage submodule-directory and commit/push). This has to be done recursively(!!!), i.e. if you change something in a submodule of a submodule (yes, that exists), you have to commit/push in the sub-submodule first, then in the submodule, then in the main repository.
2. You should not run ''git push'' anymore, but always use the ''--recurse-submodules=check'' or ''--recurse-submodules=on-demand'' flags. This can be automated by running ''git config push.recurseSubmodules check'' or ''git config push.recurseSubmodules on-demand''. This ensures that you never push the main-repo without having published all the submodule changes first.
3. If you have changed something in any of the submodules that we have not yet forked, fork it on github, change .gitmodules, run ''git submodule sync'', change the remote in the submodule. For example, see https://stackoverflow.com/a/11637270.
    I have created branches called "flw" in our submodules because normally, submodules are in a detached head state. Afterwards, I had a few issues with the remotes/origin/flw branch because it was not fetched automatically from the remote. To do so, I had to change .git/modules/<submodule>/config as described in https://git-scm.com/book/en/v2/Git-Internals-The-Refspec.

Submodules that we have forked (and configured) so far (2018-06-20):
- crazyflie-firmware
- crazyflie-lib-python
- row_ws/src/crazyflie_ros
It seems that a few more other submodules are already forked in Patrick's account, but they are not yet configured in .gitmodules.
