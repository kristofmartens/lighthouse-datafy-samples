resource "aws_iam_role" "spark_iam_role_glue" {
  name               = "spark-iam-role-glue-${var.env_name}"
  path               = "/datafy-dp-${var.env_name}/"
  assume_role_policy = data.aws_iam_policy_document.spark_iam_role_glue_assume_role.json
}

data "aws_iam_policy_document" "spark_iam_role_glue_assume_role" {
  statement {
    actions = [
      "sts:AssumeRole"
    ]
    principals {
      type        = "AWS"
      identifiers = [var.env_worker_role]
    }
    effect = "Allow"
  }
}

resource "aws_iam_role_policy" "spark_iam_role_glue" {
  name   = "spark-iam-role-glue"
  role   = aws_iam_role.spark_iam_role_glue.id
  policy = data.aws_iam_policy_document.spark_iam_role_glue.json
}

data "aws_iam_policy_document" "spark_iam_role_glue" {
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