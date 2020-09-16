locals {
  container_iam_role_s3_service_account_name = "container-iam-role-s3-${var.env_name}"
}

resource "kubernetes_service_account" "container_iam_role_s3" {
  metadata {
    name = local.container_iam_role_s3_service_account_name
    namespace = var.env_name
    annotations = {
      "eks.amazonaws.com/role-arn" : aws_iam_role.container_iam_role_s3.arn
    }
  }
  automount_service_account_token = true
}

resource "aws_iam_role" "container_iam_role_s3" {
  name               = "container-iam-role-s3-${var.env_name}"
  path               = "/datafy-dp-${var.env_name}/"
  assume_role_policy = data.aws_iam_policy_document.container_iam_role_s3_assume_role.json
}

data "aws_iam_policy_document" "container_iam_role_s3_assume_role" {
  statement {
    actions = ["sts:AssumeRoleWithWebIdentity"]
    effect  = "Allow"

    condition {
      test     = "StringEquals"
      variable = "${replace(var.aws_iam_openid_connect_provider_url, "https://", "")}:sub"
      values   = ["system:serviceaccount:${var.env_name}:${local.container_iam_role_s3_service_account_name}"]
    }

    principals {
      identifiers = [var.aws_iam_openid_connect_provider_arn]
      type        = "Federated"
    }
  }
}

resource "aws_iam_role_policy" "container_iam_role_s3" {
  name   = "container_iam_role_s3"
  role   = aws_iam_role.container_iam_role_s3.id
  policy = data.aws_iam_policy_document.container_iam_role_s3.json
}

data "aws_iam_policy_document" "container_iam_role_s3" {
  statement {
    actions = [
      "s3:*"
    ]
    resources = [
      "arn:aws:s3:::openaq-fetches",
      "arn:aws:s3:::openaq-fetches/*",
      "arn:aws:s3:::datafy-training",
      "arn:aws:s3:::datafy-training/*"
    ]
    effect = "Allow"
  }

  statement {
    actions = [
      "glue:GetDatabase"
    ]
    resources = [
      "*"
    ]
    effect = "Allow"
  }

  statement {
    actions = [
      "glue:*"
    ]
    resources = [
      "arn:aws:glue:${var.aws_region}:${var.aws_account_id}:catalog",
      "arn:aws:glue:${var.aws_region}:${var.aws_account_id}:database/airquality",
      "arn:aws:glue:${var.aws_region}:${var.aws_account_id}:table/airquality/*"
    ]
    effect = "Allow"
  }
}
