BUILDVH=../../tools/build_vendorheader
BINCTL=../../tools/headertool.py

# construct all vendor headers
for fn in *.json; do
    name=$(echo $fn | sed 's/vendor_\(.*\)\.json/\1/')
    $BUILDVH vendor_${name}.json vendor_${name}.toif vendorheader_${name}_unsigned.bin
done

# sign dev vendor header
cp -a vendorheader_unsafe_unsigned.bin vendorheader_unsafe_signed_dev.bin
$BINCTL -D vendorheader_unsafe_signed_dev.bin

cp -a vendorheader_digitshield_test_unsigned.bin vendorheader_digitshield_test_signed.bin
$BINCTL -D vendorheader_digitshield_test_signed.bin

cp -a vendorheader_digitshield_unsigned.bin vendorheader_digitshield_signed.bin