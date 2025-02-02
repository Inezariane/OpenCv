import cv2
from pyzbar.pyzbar import decode
import numpy as np
import zxing

# Create a reader instance from ZXing
barcode_reader = zxing.BarCodeReader()

# Set the image path for the Aztec barcode
img_path = "aztec.png"  
img = cv2.imread(img_path)

# Decode the barcode from the image using ZXing
result = barcode_reader.decode(img_path)

# Check if the decoding was successful
if result:
    print("Decoded Information:", result.parsed)
    print("Barcode Type:", result.format)

    # If points are available, draw them on the image
    if hasattr(result, "points") and result.points:
        try:
            # Reshape the points array for drawing
            contour_points = np.array(result.points, dtype=np.int32).reshape((-1, 1, 2))
            # Draw the boundary around the barcode
            cv2.polylines(img, [contour_points], isClosed=True, color=(0, 255, 0), thickness=2)
            
            # Place the decoded data next to the barcode
            start_x, start_y = contour_points[0][0]
            cv2.putText(img, result.parsed, (start_x, start_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        except Exception as error:
            print(f"Error with drawing the bounding box: {error}")

    # Show the image with the annotations
    cv2.imshow("Decoded Aztec Barcode", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Save the image with annotations
    output_img = "annotated_aztec.png"
    cv2.imwrite(output_img, img)
    print(f"Annotated image saved as {output_img}")

else:
    print("Aztec barcode decoding failed.")
