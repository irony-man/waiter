# App Imports
from django.conf import settings
from django.core.management import BaseCommand
from loguru import logger


class Command(BaseCommand):
    def handle(self, *args, **options):
        template = """
  async list%(apiTitle)s(ctx, query) {
    const url = getUrl("%(name)s");
    return await getRequest(url, query);
  },

  async get%(apiTitle)s(ctx, uid) {
    const url = getUrl(`%(name)s/${uid}`);
    return await getRequest(url);
  },

  async create%(apiTitle)s(ctx, formData) {
    const url = getUrl("%(name)s");
    return await postRequest(url, formData);
  },

  async update%(apiTitle)s(ctx, {uid, formData}) {
    const url = getUrl(`%(name)s/${uid}`);
    return await patchRequest(url, formData);
  },

  async createOrUpdate%(apiTitle)s(ctx, {uid, formData}) {
    return await uid?this.update%(apiTitle)s(ctx, {uid, formData}):this.create%(apiTitle)s(ctx, formData);
  },

  async delete%(apiTitle)s(ctx, uid) {
    const url = getUrl(`%(name)s/${uid}`);
    return await deleteRequest(url);
  },
"""
        result = []
        actions = {
            "chain",
            "restaurant",
            "table",
            "category",
            "menu-item",
            "order",
        }
        for name in sorted(actions):
            title = name.replace("-", " ").title().replace(" ", "")
            fmt = template % {"name": name, "apiTitle": title}
            result.append(fmt)
            logger.info(f"Actions generated for {title}.")
        functions = "\n".join(result)
        file_template = (
            """
import {
  getRequest,
  getUrl,
  postRequest,
  patchRequest,
  deleteRequest
} from "./network";

export default {
    %s
};
"""
            % functions
        )
        path = (
            settings.BASE_DIR
            / "common"
            / "static_dev"
            / "common"
            / "src"
            / "store"
            / "actions.gen.js"
        )

        with open(path, "w") as fp:
            fp.write(file_template)
            fp.flush()
