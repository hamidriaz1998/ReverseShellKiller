
echo "Starting application in background..."
docker run -d --name Reverse_Sehll_killer reverseshellkiller
echo "Application is now running in background."
echo "To view logs, run: docker logs Reverse_Sehll_killer"
echo "To stop the application, run: docker stop Reverse_Sehll_killer && docker rm Reverse_Sehll_killer"