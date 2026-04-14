output "ec2_public_ip" {
  value = aws_instance.ec2-1.public_ip
}