import { useState } from "react";
import { useMutation } from "@tanstack/react-query";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { useToast } from "@/hooks/use-toast";
import { apiRequest } from "@/lib/queryClient";
import { CheckCircle, ArrowLeft, X } from "lucide-react";

const registrationSchema = z.object({
  name: z.string().min(2, "Name must be at least 2 characters"),
  email: z.string().email("Invalid email address"),
  mobile: z.string()
    .regex(/^\d{10}$/, "Mobile number must be exactly 10 digits"),
  studentId: z.string().min(1, "Student ID is required"),
  course: z.string().min(1, "Course is required"),
  yearOfGraduation: z.string().min(1, "Year of graduation is required"),
  collegeName: z.string().min(1, "College name is required"),
  linkedinProfile: z.string().optional(),
});

type RegistrationFormData = z.infer<typeof registrationSchema>;

export default function Registration() {
  const { toast } = useToast();
  const [registrationId, setRegistrationId] = useState<string | null>(null);
  const [fieldErrors, setFieldErrors] = useState<{[key: string]: string}>({});

  const form = useForm<RegistrationFormData>({
    resolver: zodResolver(registrationSchema),
    defaultValues: {
      name: "",
      email: "",
      mobile: "",
      studentId: "",
      course: "",
      yearOfGraduation: "",
      collegeName: "",
      linkedinProfile: "",
    },
  });

  const registrationMutation = useMutation({
    mutationFn: async (data: RegistrationFormData) => {
      return await apiRequest("/api/register", {
        method: "POST",
        body: JSON.stringify(data),
      });
    },
    onSuccess: (data) => {
      setRegistrationId(data.registrationId);
      setFieldErrors({}); // Clear any field errors on success
      toast({
        title: "Registration Successful!",
        description: "Check your email for the registration confirmation.",
      });
    },
    onError: (error: any) => {
      console.log("=== REGISTRATION ERROR DEBUG ===");
      console.log("Full error object:", JSON.stringify(error, null, 2));
      console.log("Error message:", error.message);
      console.log("Error status:", error.status);
      console.log("Error fieldErrors:", error.fieldErrors);
      console.log("Error keys:", Object.keys(error));
      
      // Clear previous field errors
      setFieldErrors({});
      
      let shouldSuppressToast = false;
      const newFieldErrors: {[key: string]: string} = {};
      
      // First priority: Check if the error response contains field-specific errors
      if (error.fieldErrors && typeof error.fieldErrors === 'object' && Object.keys(error.fieldErrors).length > 0) {
        console.log("✅ Found server fieldErrors:", error.fieldErrors);
        Object.assign(newFieldErrors, error.fieldErrors);
        shouldSuppressToast = true;
      } 
      
      // Second priority: Parse error message for known patterns
      if (error.message && typeof error.message === 'string') {
        const errorMessage = error.message.toLowerCase();
        console.log("Checking error message:", errorMessage);
        
        if (errorMessage.includes('email') && errorMessage.includes('registered')) {
          console.log("✅ Detected email registration error");
          newFieldErrors.email = 'Email already registered';
          shouldSuppressToast = true;
        }
        if (errorMessage.includes('mobile') && errorMessage.includes('registered')) {
          console.log("✅ Detected mobile registration error");
          newFieldErrors.mobile = 'Mobile number already registered';
          shouldSuppressToast = true;
        }
      }
      
      // If we have field errors, set them and suppress toast
      if (shouldSuppressToast && Object.keys(newFieldErrors).length > 0) {
        console.log("✅ Setting field errors and suppressing toast:", newFieldErrors);
        setFieldErrors(newFieldErrors);
        console.log("=== TOAST SUPPRESSED ===");
        return; // Exit early - NO TOAST
      }
      
      // Only show toast for non-field-specific errors
      console.log("❌ No field errors detected, showing toast");
      console.log("=== SHOWING TOAST ===");
      toast({
        title: "Registration Failed",
        description: error.message || "An error occurred during registration. Please try again.",
        variant: "destructive",
      });
    },
  });

  const onSubmit = (data: RegistrationFormData) => {
    setFieldErrors({}); // Clear field errors when submitting
    registrationMutation.mutate(data);
  };

  const clearFieldError = (fieldName: string) => {
    if (fieldErrors[fieldName]) {
      setFieldErrors(prev => {
        const newErrors = { ...prev };
        delete newErrors[fieldName];
        return newErrors;
      });
    }
  };

  if (registrationId) {
    return (
      <div className="min-h-screen bg-slate-50 flex items-center justify-center p-4">
        <Card className="w-full max-w-md">
          <CardHeader className="text-center">
            <div className="w-16 h-16 bg-emerald-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <CheckCircle className="w-8 h-8 text-emerald-600" />
            </div>
            <CardTitle className="text-emerald-700">Registration Successful!</CardTitle>
          </CardHeader>
          <CardContent className="text-center space-y-4">
            <div className="bg-slate-50 rounded-lg p-4">
              <p className="text-sm text-slate-600 mb-2">Your Registration ID</p>
              <p className="font-mono text-lg font-bold text-slate-900">{registrationId}</p>
            </div>
            <p className="text-slate-600">
              A confirmation email has been sent to your registered email address. 
              Please keep your Registration ID safe for future reference.
            </p>
            <div className="space-y-2">
              <Button 
                onClick={() => window.location.href = '/'}
                className="w-full"
              >
                <ArrowLeft className="w-4 h-4 mr-2" />
                Back to Home
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-50 py-12">
      <div className="container mx-auto px-4 max-w-2xl">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-slate-900 mb-2">Hackathon Registration</h1>
          <p className="text-slate-600">
            Fill in your details to register for the hackathon event
          </p>
        </div>

        <Card>
          <CardHeader>
            <CardTitle>Registration Form</CardTitle>
          </CardHeader>
          <CardContent>
            <Form {...form}>
              <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <FormField
                    control={form.control}
                    name="name"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>Full Name</FormLabel>
                        <FormControl>
                          <Input placeholder="Enter your full name" {...field} />
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />

                  <FormField
                    control={form.control}
                    name="email"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>Email Address</FormLabel>
                        <FormControl>
                          <div className="relative">
                            <Input 
                              type="email" 
                              placeholder="your.email@example.com" 
                              {...field} 
                              className={fieldErrors.email ? "border-red-500 focus:border-red-500 pr-10" : ""}
                              onChange={(e) => {
                                field.onChange(e);
                                clearFieldError('email');
                              }}
                            />
                            {fieldErrors.email && (
                              <X 
                                className="absolute right-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-red-500 cursor-pointer hover:text-red-600 transition-colors" 
                                onClick={() => {
                                  field.onChange('');
                                  clearFieldError('email');
                                }}
                              />
                            )}
                          </div>
                        </FormControl>
                        {fieldErrors.email ? (
                          <p className="text-sm text-red-500 mt-1">{fieldErrors.email}</p>
                        ) : (
                          <FormMessage />
                        )}
                      </FormItem>
                    )}
                  />

                  <FormField
                    control={form.control}
                    name="mobile"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>Mobile Number</FormLabel>
                        <FormControl>
                          <div className="relative">
                            <Input 
                              placeholder="+91 1234567890" 
                              {...field} 
                              className={fieldErrors.mobile ? "border-red-500 focus:border-red-500 pr-10" : ""}
                              onChange={(e) => {
                                field.onChange(e);
                                clearFieldError('mobile');
                              }}
                            />
                            {fieldErrors.mobile && (
                              <X 
                                className="absolute right-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-red-500 cursor-pointer hover:text-red-600 transition-colors" 
                                onClick={() => {
                                  field.onChange('');
                                  clearFieldError('mobile');
                                }}
                              />
                            )}
                          </div>
                        </FormControl>
                        {fieldErrors.mobile ? (
                          <p className="text-sm text-red-500 mt-1">{fieldErrors.mobile}</p>
                        ) : (
                          <FormMessage />
                        )}
                      </FormItem>
                    )}
                  />

                  <FormField
                    control={form.control}
                    name="studentId"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>Student ID</FormLabel>
                        <FormControl>
                          <Input placeholder="Your student ID" {...field} />
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />

                  <FormField
                    control={form.control}
                    name="course"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>Course</FormLabel>
                        <FormControl>
                          <Select onValueChange={field.onChange} value={field.value}>
                            <SelectTrigger>
                              <SelectValue placeholder="Select your course" />
                            </SelectTrigger>
                            <SelectContent>
                              <SelectItem value="Computer Science Engineering">Computer Science Engineering</SelectItem>
                              <SelectItem value="Information Technology">Information Technology</SelectItem>
                              <SelectItem value="Electronics and Communication">Electronics and Communication</SelectItem>
                              <SelectItem value="Mechanical Engineering">Mechanical Engineering</SelectItem>
                              <SelectItem value="Civil Engineering">Civil Engineering</SelectItem>
                              <SelectItem value="Electrical Engineering">Electrical Engineering</SelectItem>
                              <SelectItem value="Other">Other</SelectItem>
                            </SelectContent>
                          </Select>
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />

                  <FormField
                    control={form.control}
                    name="yearOfGraduation"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>Year of Graduation</FormLabel>
                        <FormControl>
                          <Select onValueChange={field.onChange} value={field.value}>
                            <SelectTrigger>
                              <SelectValue placeholder="Select year" />
                            </SelectTrigger>
                            <SelectContent>
                              <SelectItem value="2024">2024</SelectItem>
                              <SelectItem value="2025">2025</SelectItem>
                              <SelectItem value="2026">2026</SelectItem>
                              <SelectItem value="2027">2027</SelectItem>
                              <SelectItem value="2028">2028</SelectItem>
                            </SelectContent>
                          </Select>
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                </div>

                <FormField
                  control={form.control}
                  name="collegeName"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>College Name</FormLabel>
                      <FormControl>
                        <Input placeholder="Enter your college/university name" {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />

                <FormField
                  control={form.control}
                  name="linkedinProfile"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>LinkedIn Profile <span className="text-slate-400">(Optional)</span></FormLabel>
                      <FormControl>
                        <Input placeholder="https://linkedin.com/in/yourprofile" {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />

                <div className="flex items-center justify-between pt-4">
                  <Button 
                    type="button" 
                    variant="outline"
                    onClick={() => window.location.href = '/'}
                  >
                    <ArrowLeft className="w-4 h-4 mr-2" />
                    Back to Home
                  </Button>
                  <Button 
                    type="submit" 
                    disabled={registrationMutation.isPending}
                    className="bg-blue-600 hover:bg-blue-700"
                  >
                    {registrationMutation.isPending ? "Registering..." : "Register"}
                  </Button>
                </div>
              </form>
            </Form>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
